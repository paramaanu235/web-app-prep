# Java design patterns cheat sheet

Java 8 language/API baseline. In an interview, explain the problem, name the pattern when useful, and sketch the relevant collaboration. Scale the code to the problem rather than targeting a fixed line count.

**How to read a pattern:** intent → when → code → pitfall.

**GoF groups:** Creational (how objects are born) · Structural (how objects are composed) · Behavioral (how objects talk).

The original GoF catalog has 23 patterns. Object Pool (section 6) and sections 25–33 are additional patterns or design techniques. Unless explicitly synchronized, concurrent, or immutable, examples assume single-threaded use. These are teaching examples, not production implementations.

```sh
# Save ONE entire Java block as SingletonDemo.java (for section 1).
# Keep the classes top-level; the block already includes a main method.
javac --release 8 SingletonDemo.java
java SingletonDemo
```

For other sections, use the demo class's actual name. Use a separate directory per pattern because examples reuse names such as `User`. `--release 8` requires JDK 9+; on JDK 8 itself, omit that option.

**Validation, 7 September 2026:** All 33 Java blocks were extracted into separate directories, compiled with `javac --release 8` on JDK 25, and their demo programs ran successfully. Fourteen patterns also passed 957 targeted checks covering boundary conditions, typed lookup, value equality, XML parsing, pool ownership/reset, concurrent singleton/flyweight access, callback mutation, failed undo retention, snapshot encapsulation, and producer–consumer interruption cleanup. These are example-level checks, not proof of production readiness or every possible thread interleaving.

---

## Index

**Creational**
- [Singleton](#1-singleton)
- [Factory Method](#2-factory-method)
- [Abstract Factory](#3-abstract-factory)
- [Builder](#4-builder)
- [Prototype](#5-prototype)
- [Object Pool — extra, not GoF](#6-object-pool)

**Structural**
- [Adapter](#7-adapter)
- [Bridge](#8-bridge)
- [Composite](#9-composite)
- [Decorator](#10-decorator)
- [Facade](#11-facade)
- [Flyweight](#12-flyweight)
- [Proxy](#13-proxy)

**Behavioral**
- [Chain of Responsibility](#14-chain-of-responsibility)
- [Command](#15-command)
- [Interpreter](#16-interpreter)
- [Iterator](#17-iterator)
- [Mediator](#18-mediator)
- [Memento](#19-memento)
- [Observer](#20-observer)
- [State](#21-state)
- [Strategy](#22-strategy)
- [Template Method](#23-template-method)
- [Visitor](#24-visitor)

**Java / interview extras**
- [Null Object](#25-null-object)
- [DAO / Repository](#26-dao--repository)
- [Dependency Injection](#27-dependency-injection)
- [MVC](#28-mvc)
- [Producer–Consumer](#29-producerconsumer)
- [Immutable object](#30-immutable-object)
- [Marker interface](#31-marker-interface)
- [Front Controller](#32-front-controller)
- [Service Locator (usually an anti-pattern)](#33-service-locator)

**Quick pick:** [When which pattern](#when-which-pattern)

---

## 1. Singleton

**Intent:** One instance of the singleton type per defining class loader, with a shared access point; not one instance across every JVM or class loader.

**When:** Config, metrics client, thread pool coordinator — not “I need globals.”

**Interview answer:** An enum resists ordinary reflective construction and preserves identity during Java serialization. The initialization-on-demand holder idiom provides lazy class initialization without hand-written locking. Double-checked locking is another option when implemented correctly with `volatile`.

```java
enum AppConfig {
    INSTANCE;
    private final String env = System.getProperty("env", "prod");
    public String env() { return env; }
}

final class LazyHolderConfig {
    private LazyHolderConfig() {}
    private static class Holder {
        static final LazyHolderConfig I = new LazyHolderConfig();
    }
    public static LazyHolderConfig get() { return Holder.I; }
}

final class DclConfig {
    private static volatile DclConfig instance;
    private DclConfig() {}
    public static DclConfig get() {
        DclConfig local = instance;
        if (local == null) {
            synchronized (DclConfig.class) {
                local = instance;
                if (local == null) instance = local = new DclConfig();
            }
        }
        return local;
    }
}

class SingletonDemo {
    public static void main(String[] args) {
        System.out.println(AppConfig.INSTANCE.env());
        System.out.println(LazyHolderConfig.get() == LazyHolderConfig.get()); // true
        System.out.println(DclConfig.get() == DclConfig.get());               // true
    }
}
```

**Pitfall:** A synchronized accessor is correct; whether its overhead matters depends on workload and contention. DCL requires the `volatile` publication shown here. Instance creation safety does not make mutable singleton methods thread-safe. Shared global access can hide dependencies; constructor injection makes those dependencies explicit.

---

## 2. Factory Method

**Intent:** Subclasses decide *which* concrete product to create. Client depends on the product interface.

**When:** A creator's workflow should call an overridable creation method, letting subclasses select the product. A discriminator-based static factory alone is a Simple Factory.

```java
interface Notifier { void send(String to, String body); }

final class EmailNotifier implements Notifier {
    public void send(String to, String body) {
        System.out.println("email -> " + to + ": " + body);
    }
}
final class SmsNotifier implements Notifier {
    public void send(String to, String body) {
        System.out.println("sms -> " + to + ": " + body);
    }
}

abstract class AlertService {
    abstract Notifier createNotifier();          // factory method
    void alert(String to, String body) {
        createNotifier().send(to, body);
    }
}
final class EmailAlertService extends AlertService {
    Notifier createNotifier() { return new EmailNotifier(); }
}
final class SmsAlertService extends AlertService {
    Notifier createNotifier() { return new SmsNotifier(); }
}

class FactoryMethodDemo {
    public static void main(String[] args) {
        AlertService svc = new SmsAlertService();
        svc.alert("+1555", "disk 90%");
    }
}
```

**Pitfall:** A static `NotifierFactory.create("sms")` is a **Simple Factory**, not GoF Factory Method. If creator subclasses add no value, a registry or injected factory may be simpler. Abstract Factory addresses related product families; it does not automatically solve subclass proliferation.

---

## 3. Abstract Factory

**Intent:** Create a *family* of related products (button + checkbox of the same look) without naming concretes.

**When:** Multiple products must match as a family. The database types below are fake teaching interfaces, not JDBC or Google Cloud client APIs; Bigtable's limit description is not executable SQL.

```java
interface Connection { String kind(); }
interface Dialect { String limit(int n); }

final class PgConnection implements Connection {
    public String kind() { return "postgres"; }
}
final class PgDialect implements Dialect {
    public String limit(int n) { return " LIMIT " + n; }
}
final class BtConnection implements Connection {
    public String kind() { return "bigtable"; }
}
final class BtDialect implements Dialect {
    public String limit(int n) { return " row-limit=" + n; } // descriptive placeholder
}

interface DbFactory {
    Connection connection();
    Dialect dialect();
}
final class PostgresFactory implements DbFactory {
    public Connection connection() { return new PgConnection(); }
    public Dialect dialect() { return new PgDialect(); }
}
final class BigtableFactory implements DbFactory {
    public Connection connection() { return new BtConnection(); }
    public Dialect dialect() { return new BtDialect(); }
}

final class QueryRunner {
    private final DbFactory factory;
    QueryRunner(DbFactory factory) { this.factory = factory; }
    void run() {
        System.out.println(factory.connection().kind() + factory.dialect().limit(10));
    }
}

class AbstractFactoryDemo {
    public static void main(String[] args) {
        new QueryRunner(new PostgresFactory()).run(); // postgres LIMIT 10
        new QueryRunner(new BigtableFactory()).run(); // bigtable row-limit=10 (description)
    }
}
```

**Pitfall:** Adding a new product type (e.g. `Migrator`) forces every factory to change. If families are unstable, this is the wrong pattern.

---

## 4. Builder

**Intent:** Construct a complex immutable object step by step. Telescoping constructors go away.

**When:** Construction has several optional choices or cross-field constraints. A builder can validate at `build()` time; this ordinary builder does not make invalid states unrepresentable at compile time.

```java
final class HttpRequest {
    final String method, url, body;
    final int timeoutMs;
    private HttpRequest(Builder b) {
        this.method = b.method;
        this.url = b.url;
        this.body = b.body;
        this.timeoutMs = b.timeoutMs;
    }
    static final class Builder {
        private String method = "GET";
        private String url;
        private String body = "";
        private int timeoutMs = 1000;
        Builder url(String url) { this.url = url; return this; }
        Builder method(String m) { this.method = m; return this; }
        Builder body(String b) { this.body = b; return this; }
        Builder timeoutMs(int t) { this.timeoutMs = t; return this; }
        HttpRequest build() {
            if (url == null || url.trim().isEmpty()) throw new IllegalStateException("url");
            if (method == null || method.trim().isEmpty()) throw new IllegalStateException("method");
            if (body == null) throw new IllegalStateException("body");
            if (timeoutMs <= 0) throw new IllegalStateException("timeout must be positive");
            return new HttpRequest(this);
        }
    }
    public String toString() { return method + " " + url + " t=" + timeoutMs; }
}

class BuilderDemo {
    public static void main(String[] args) {
        HttpRequest r = new HttpRequest.Builder()
                .url("https://example.com")
                .method("POST")
                .body("{\"q\":1}")
                .timeoutMs(250)
                .build();
        System.out.println(r);
    }
}
```

**Pitfall:** Builders are mutable; this product contains only immutable strings and primitive fields. Validate invariants explicitly and defensively copy mutable inputs. These checks illustrate construction validation, not a full HTTP/URL validator. This fluent builder is a common Java variation; not every builder must produce an immutable object.

---

## 5. Prototype

**Intent:** Copy an existing object instead of constructing from scratch (especially if construction is expensive or hidden).

**When:** Many similar objects, clone cheaper than `new` + setup. Java: `Cloneable` is hostile — prefer a copy constructor.

```java
final class ReportTemplate {
    final String title;
    final java.util.List<String> sections;
    ReportTemplate(String title, java.util.List<String> sections) {
        this.title = title;
        this.sections = new java.util.ArrayList<String>(sections);
    }
    ReportTemplate copy() {                         // prototype
        return new ReportTemplate(title, sections); // new list; immutable Strings shared
    }
}

class PrototypeDemo {
    public static void main(String[] args) {
        ReportTemplate proto = new ReportTemplate("Q3", java.util.Arrays.asList("rev", "cost"));
        ReportTemplate west = proto.copy();
        west.sections.add("west-only");
        System.out.println(proto.sections); // [rev, cost]  — original intact
        System.out.println(west.sections);  // [rev, cost, west-only]
    }
}
```

**Pitfall:** `Object.clone()` performs a shallow field copy and checks `Cloneable`; it does not itself copy referenced mutable objects. Choose the intended sharing depth explicitly. Here a new list plus shared immutable Strings gives independent section-list edits. Copy constructors/factories usually make that policy clearer.

---

## 6. Object Pool

**Intent:** Reuse expensive instances (connections, buffers) instead of allocate/free churn.

**When:** Object creation is costly and cardinality is bounded.

```java
final class BufferPool {
    private final java.util.Deque<byte[]> free = new java.util.ArrayDeque<byte[]>();
    private final java.util.Set<byte[]> borrowed = java.util.Collections.newSetFromMap(
            new java.util.IdentityHashMap<byte[], Boolean>());
    BufferPool(int size, int bufBytes) {
        if (size <= 0 || bufBytes <= 0) throw new IllegalArgumentException("positive sizes required");
        for (int i = 0; i < size; i++) free.offer(new byte[bufBytes]);
    }
    synchronized byte[] acquire() {
        byte[] b = free.poll();
        if (b == null) throw new IllegalStateException("pool exhausted"); // bounded, fail-fast policy
        borrowed.add(b);
        return b;
    }
    synchronized void release(byte[] b) {
        if (!borrowed.remove(b)) throw new IllegalArgumentException("foreign or already released buffer");
        java.util.Arrays.fill(b, (byte) 0);
        free.offer(b);
    }
}

class PoolDemo {
    public static void main(String[] args) {
        BufferPool pool = new BufferPool(2, 8);
        byte[] a = pool.acquire();
        try { a[0] = 42; }
        finally { pool.release(a); }
        byte[] b = pool.acquire();
        try { System.out.println(b[0]); } // 0
        finally { pool.release(b); }
    }
}
```

**Pitfall:** Define exhaustion policy: this fixed-size pool fails fast instead of silently allocating a differently sized buffer. Release validates identity and resets contents. Callers must release exactly once, stop using references after release, and own each checked-out buffer exclusively. Synchronization protects pool bookkeeping, not arbitrary access to the byte arrays. A production lease API can make ownership clearer; block or time out only if that is the intended policy. Pool expensive resources when measurements justify it, not every cheap object.

---

## 7. Adapter

**Intent:** Make an existing class match the interface the client already uses. “Wrapper that translates.”

**When:** An existing API differs from the interface the client should use. An adapter can preserve a stable client interface even when changing that client would be technically possible.

```java
interface JsonStore { void put(String key, String json); }

final class LegacyXmlStore {
    void saveXml(String id, String xml) {
        System.out.println("xml[" + id + "]=" + xml);
    }
}

final class JsonToXmlAdapter implements JsonStore {
    private final LegacyXmlStore legacy;
    JsonToXmlAdapter(LegacyXmlStore legacy) { this.legacy = legacy; }
    public void put(String key, String json) {
        // Store valid JSON text as XML text content, not a structural JSON-to-XML mapping.
        String escaped = json.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
        legacy.saveXml(key, "<x>" + escaped + "</x>");
    }
}

class AdapterDemo {
    public static void main(String[] args) {
        JsonStore store = new JsonToXmlAdapter(new LegacyXmlStore());
        store.put("u1", "{\"n\":1}");
    }
}
```

**Pitfall:** Adapter ≠ Facade (facade simplifies a subsystem) ≠ Decorator (decorator adds behavior, same interface) ≠ Proxy (same interface, controls access). `Arrays.asList` / `InputStreamReader` are adapters.

---

## 8. Bridge

**Intent:** Split **abstraction** from **implementation** so they vary independently (two class hierarchies, not a cartesian product).

**When:** `CircleRaster`, `CircleVector`, `SquareRaster`, `SquareVector`… explode. Decouple shape × renderer.

```java
interface Renderer { void draw(String shape); }
final class RasterRenderer implements Renderer {
    public void draw(String shape) { System.out.println("pixels:" + shape); }
}
final class VectorRenderer implements Renderer {
    public void draw(String shape) { System.out.println("paths:" + shape); }
}

abstract class Shape {
    final Renderer renderer;
    Shape(Renderer renderer) { this.renderer = renderer; }
    abstract void draw();
}
final class Circle extends Shape {
    Circle(Renderer r) { super(r); }
    void draw() { renderer.draw("circle"); }
}
final class Square extends Shape {
    Square(Renderer r) { super(r); }
    void draw() { renderer.draw("square"); }
}

class BridgeDemo {
    public static void main(String[] args) {
        new Circle(new VectorRenderer()).draw(); // paths:circle
        new Square(new RasterRenderer()).draw(); // pixels:square
    }
}
```

**Pitfall:** People confuse Bridge with Adapter. Adapter wraps an *already written* class. Bridge is designed up front so two dimensions evolve separately. JDBC (`Driver` vs `Connection` usage) is loosely this idea.

---

## 9. Composite

**Intent:** Treat a single object and a tree of objects uniformly.

**When:** File/folder, org chart, UI view tree, expression tree.

```java
interface FileSys {
    int size();
    void print(String indent);
}
final class FileLeaf implements FileSys {
    final String name; final int bytes;
    FileLeaf(String name, int bytes) { this.name = name; this.bytes = bytes; }
    public int size() { return bytes; }
    public void print(String indent) { System.out.println(indent + name + " " + bytes); }
}
final class Folder implements FileSys {
    final String name;
    final java.util.List<FileSys> kids = new java.util.ArrayList<FileSys>();
    Folder(String name) { this.name = name; }
    Folder add(FileSys c) { kids.add(c); return this; }
    public int size() {
        int s = 0;
        for (FileSys c : kids) s += c.size();
        return s;
    }
    public void print(String indent) {
        System.out.println(indent + name + "/");
        for (FileSys c : kids) c.print(indent + "  ");
    }
}

class CompositeDemo {
    public static void main(String[] args) {
        Folder root = new Folder("src")
                .add(new FileLeaf("A.java", 10))
                .add(new Folder("util").add(new FileLeaf("B.java", 5)));
        root.print("");
        System.out.println("total=" + root.size()); // 15
    }
}
```

**Pitfall:** This example assumes an acyclic tree and totals fitting in `int`. On a DAG, decide whether to count each occurrence or each distinct object; use a visited identity set for the latter. Interning alone does not prevent repeated counting. Cycles require detection, and deep trees may require iterative traversal. Real byte totals often need `long`.

---

## 10. Decorator

**Intent:** Add behavior to an object at runtime by wrapping it, without exploding subclasses.

**When:** Streams (`BufferedInputStream(new GZIPInputStream(...))`), auth + logging + metrics around a service.

```java
interface Coffee { int cost(); String desc(); }
final class Espresso implements Coffee {
    public int cost() { return 2; }
    public String desc() { return "espresso"; }
}
abstract class CoffeeDecorator implements Coffee {
    final Coffee inner;
    CoffeeDecorator(Coffee inner) { this.inner = inner; }
}
final class Milk extends CoffeeDecorator {
    Milk(Coffee c) { super(c); }
    public int cost() { return inner.cost() + 1; }
    public String desc() { return inner.desc() + "+milk"; }
}
final class Whip extends CoffeeDecorator {
    Whip(Coffee c) { super(c); }
    public int cost() { return inner.cost() + 1; }
    public String desc() { return inner.desc() + "+whip"; }
}

class DecoratorDemo {
    public static void main(String[] args) {
        Coffee c = new Whip(new Milk(new Espresso()));
        System.out.println(c.desc() + " $" + c.cost()); // espresso+milk+whip $4
    }
}
```

**Pitfall:** A wrapper has a different reference identity from the wrapped object; equality/hash-code semantics must be deliberate, not assumed. This does not inherently violate the hash-code contract. Wrapping order matters when behaviors are not commutative. Java I/O streams are a useful example.

---

## 11. Facade

**Intent:** One simple API in front of a messy subsystem.

**When:** Client should not know about connection pooling, retries, serialization.

```java
final class Inventory { boolean reserve(String sku) { return true; } }
final class Payments { void charge(String user, int cents) { System.out.println("charged " + cents); } }
final class Shipping { void ship(String sku, String user) { System.out.println("ship " + sku + " -> " + user); } }

final class CheckoutFacade {
    private final Inventory inventory = new Inventory();
    private final Payments payments = new Payments();
    private final Shipping shipping = new Shipping();
    void buy(String user, String sku, int cents) {
        if (!inventory.reserve(sku)) throw new IllegalStateException("stock");
        payments.charge(user, cents);
        shipping.ship(sku, user);
    }
}

class FacadeDemo {
    public static void main(String[] args) {
        new CheckoutFacade().buy("u1", "sku-9", 499);
    }
}
```

**Pitfall:** Keep the facade focused on a use case. It can coordinate behavior as well as simplify access. This checkout is a happy-path illustration: a facade does not make reservation, payment, and shipping atomic. Real failures require explicit retry, idempotency, and compensation/transaction decisions.

---

## 12. Flyweight

**Intent:** Share *intrinsic* (immutable) state across many objects; keep *extrinsic* state outside.

**When:** Millions of similar objects (glyphs, map tiles, tree species). Memory bound.

```java
final class TreeType {                 // intrinsic, shared
    final String name, texture;
    TreeType(String name, String texture) { this.name = name; this.texture = texture; }
    void draw(int x, int y) { System.out.println(name + "@" + x + "," + y); }
}
final class TreeFactory {
    private static final java.util.concurrent.ConcurrentMap<java.util.List<String>, TreeType> CACHE =
            new java.util.concurrent.ConcurrentHashMap<java.util.List<String>, TreeType>();
    static TreeType type(String name, String texture) {
        java.util.Objects.requireNonNull(name);
        java.util.Objects.requireNonNull(texture);
        // The private key is never mutated or exposed; fields are immutable strings.
        java.util.List<String> key = java.util.Collections.unmodifiableList(java.util.Arrays.asList(name, texture));
        return CACHE.computeIfAbsent(key, k -> new TreeType(name, texture));
    }
}
final class Tree {                     // extrinsic: position
    final int x, y;
    final TreeType type;
    Tree(int x, int y, TreeType type) { this.x = x; this.y = y; this.type = type; }
    void draw() { type.draw(x, y); }
}

class FlyweightDemo {
    public static void main(String[] args) {
        TreeType oak = TreeFactory.type("oak", "oak.png");
        new Tree(1, 2, oak).draw();
        new Tree(3, 4, oak).draw();
        System.out.println(TreeFactory.type("oak", "oak.png") == oak); // true, shared
    }
}
```

**Pitfall:** Share intrinsic state safely, normally by making it immutable. Composite keys avoid delimiter collisions such as `(a|b,c)` versus `(a,b|c)`, and atomic cache insertion preserves sharing across concurrent callers. This static cache retains entries indefinitely; bound or scope its lifetime for unbounded inputs. Wrapper caches and string interning illustrate reuse, but compare wrapper values with `equals`, not reference identity.

---

## 13. Proxy

**Intent:** Same interface as the real object; control access (lazy, remote, security, logging).

**When:** Virtual proxy (lazy expensive object), protection proxy (auth), remote proxy (stub), smart reference (refcount).

```java
interface Image { void display(); }

final class RealImage implements Image {
    private final String path;
    RealImage(String path) { this.path = path; load(); }
    private void load() { System.out.println("load disk " + path); }
    public void display() { System.out.println("show " + path); }
}

final class LazyImageProxy implements Image {
    private final String path;
    private RealImage real;
    LazyImageProxy(String path) { this.path = path; }
    public void display() {
        if (real == null) real = new RealImage(path); // create on first use
        real.display();
    }
}

class ProxyDemo {
    public static void main(String[] args) {
        Image img = new LazyImageProxy("/big.png");
        System.out.println("constructed, not loaded");
        img.display(); // load + show
        img.display(); // show only
    }
}
```

**Pitfall:** This lazy proxy is single-threaded: concurrent first access could construct multiple images. Add suitable synchronization if shared. JDK dynamic proxies implement interfaces; other proxy mechanisms can subclass classes. A proxy controls access through the target abstraction, while an adapter translates to a different client-facing abstraction.

---

## 14. Chain of Responsibility

**Intent:** Pass a request through ordered handlers. This example stops at the first handler that accepts it; filter pipelines may instead invoke several handlers around a downstream call.

**When:** Logging levels, servlet filters, approval workflows, exception handlers.

```java
abstract class Handler {
    Handler next;
    Handler then(Handler n) { next = n; return n; }
    void handle(int amount) {
        if (amount < 0) throw new IllegalArgumentException("amount must be nonnegative");
        if (canHandle(amount)) doHandle(amount);
        else if (next != null) next.handle(amount);
        else System.out.println("unhandled " + amount);
    }
    abstract boolean canHandle(int amount);
    abstract void doHandle(int amount);
}
final class Manager extends Handler {
    boolean canHandle(int a) { return a <= 1000; }
    void doHandle(int a) { System.out.println("manager ok " + a); }
}
final class Director extends Handler {
    boolean canHandle(int a) { return a <= 10000; }
    void doHandle(int a) { System.out.println("director ok " + a); }
}

class ChainDemo {
    public static void main(String[] args) {
        Handler h = new Manager();
        h.then(new Director());
        h.handle(500);
        h.handle(5000);
        h.handle(50000);
    }
}
```

**Pitfall:** The chain must be acyclic and terminate; its configured order changes behavior. `then` returns the newly linked handler, so retain the original head when building a longer chain. Servlet filters illustrate a related pass-through variant rather than necessarily first-match handling.

---

## 15. Command

**Intent:** Encapsulate a request as an object (execute / undo / queue / log).

**When:** Undo, job queues, macro recording, GUI actions, transactional outbox.

```java
interface Command { void execute(); void undo(); }

final class Editor {
    final StringBuilder text = new StringBuilder();
}
final class InsertCmd implements Command {
    private final Editor editor;
    private final String chunk;
    private int start;
    private boolean applied;
    InsertCmd(Editor e, String chunk) {
        this.editor = java.util.Objects.requireNonNull(e);
        this.chunk = java.util.Objects.requireNonNull(chunk);
    }
    public void execute() {
        if (applied) throw new IllegalStateException("already applied");
        start = editor.text.length();
        editor.text.append(chunk);
        applied = true;
    }
    public void undo() {
        // Single-threaded LIFO history; edits must go through that history.
        if (!applied || editor.text.length() != start + chunk.length()
                || !editor.text.substring(start).equals(chunk))
            throw new IllegalStateException("not the current edit");
        editor.text.delete(start, editor.text.length());
        applied = false;
    }
}

final class Invoker {
    private final java.util.Deque<Command> history = new java.util.ArrayDeque<Command>();
    void run(Command c) { c.execute(); history.push(c); }
    void undo() {
        if (!history.isEmpty()) {
            history.peek().undo(); // keep the entry if undo fails
            history.pop();
        }
    }
}

class CommandDemo {
    public static void main(String[] args) {
        Editor ed = new Editor();
        Invoker inv = new Invoker();
        inv.run(new InsertCmd(ed, "Hello"));
        inv.run(new InsertCmd(ed, "!"));
        System.out.println(ed.text); // Hello!
        inv.undo();
        System.out.println(ed.text); // Hello
    }
}
```

**Pitfall:** This append command assumes single-threaded, LIFO undo and no untracked edits; it can be re-executed after a successful undo. More general editors need stronger history/version rules. Choose snapshots or deltas according to operation semantics and cost. A command object does not automatically provide transactional rollback or retry idempotency. `Runnable` illustrates an executable command without undo.

---

## 16. Interpreter

**Intent:** Given a language, represent grammar as a tree and evaluate it.

**When:** Small grammars or expression/rule trees. Larger languages may use handwritten parsers or parser generators; their interpreters and compilers can still operate on ASTs. This demo constructs the tree directly, without parsing text.

```java
interface Expr { int eval(); }
final class Num implements Expr {
    final int v;
    Num(int v) { this.v = v; }
    public int eval() { return v; }
}
final class Add implements Expr {
    final Expr l, r;
    Add(Expr l, Expr r) { this.l = l; this.r = r; }
    public int eval() { return l.eval() + r.eval(); }
}
final class Mul implements Expr {
    final Expr l, r;
    Mul(Expr l, Expr r) { this.l = l; this.r = r; }
    public int eval() { return l.eval() * r.eval(); }
}

class InterpreterDemo {
    public static void main(String[] args) {
        Expr e = new Add(new Num(2), new Mul(new Num(3), new Num(4))); // 2+3*4
        System.out.println(e.eval()); // 14
    }
}
```

**Pitfall:** This GoF example models grammar rules as classes; it is not a full language implementation. New syntax may require new AST node types. Visitor helps add operations to a stable node set; it does not remove that cost. The arithmetic demo assumes results fit `int`; use checked arithmetic or a different numeric type if required.

---

## 17. Iterator

**Intent:** Access elements of a collection without exposing representation.

**When:** You already use this every day (`for-each`, `Iterator`). Write one when you have a custom structure.

```java
final class Range implements Iterable<Integer> {
    private final int start, end; // [start, end)
    Range(int start, int end) { this.start = start; this.end = end; }
    public java.util.Iterator<Integer> iterator() {
        return new java.util.Iterator<Integer>() {
            int cur = start;
            public boolean hasNext() { return cur < end; }
            public Integer next() {
                if (!hasNext()) throw new java.util.NoSuchElementException();
                return cur++;
            }
            public void remove() { throw new UnsupportedOperationException(); }
        };
    }
}

class IteratorDemo {
    public static void main(String[] args) {
        for (int x : new Range(3, 6)) System.out.print(x + " "); // 3 4 5
    }
}
```

**Pitfall:** `next()` must throw `NoSuchElementException` on exhaustion. This immutable Range gives each iterator an independent cursor. For mutable collections, fail-fast detection is best-effort, not a synchronization guarantee. Direct collection removal during enhanced-for may invalidate its iterator; use the iterator's optional `remove()` when supported, or a snapshot. [Iterator contract](https://docs.oracle.com/javase/8/docs/api/java/util/Iterator.html)

---

## 18. Mediator

**Intent:** Objects don’t talk pairwise; they talk through one mediator. Cuts n² coupling.

**When:** Chat room, air-traffic control, UI widget coordination, dialog boxes.

```java
interface ChatMediator { void send(User from, String msg); void join(User u); }
final class User {
    final String name;
    final ChatMediator room;
    User(String name, ChatMediator room) { this.name = name; this.room = room; room.join(this); }
    void say(String msg) { room.send(this, msg); }
    void recv(User from, String msg) {
        if (from != this) System.out.println(name + " heard " + from.name + ": " + msg);
    }
}
final class ChatRoom implements ChatMediator {
    private final java.util.List<User> users = new java.util.ArrayList<User>();
    public void join(User u) { users.add(u); }
    public void send(User from, String msg) {
        for (User u : users) u.recv(from, msg);
    }
}

class MediatorDemo {
    public static void main(String[] args) {
        ChatRoom room = new ChatRoom();
        User a = new User("Ann", room), b = new User("Bob", room);
        a.say("hi");
    }
}
```

**Pitfall:** A mediator can become an oversized coordinator. This in-process, single-threaded chat excludes the sender by object identity, not display name, so distinct users may share a name. Real membership/authentication/lifecycle policies are omitted. Mediator coordinates colleagues; Observer manages notification subscriptions. Their implementations can overlap.

---

## 19. Memento

**Intent:** Capture internal state so you can restore it, without breaking encapsulation.

**When:** Undo, snapshots, transactional rollback of an object.

```java
final class Doc {
    static final class Memento {
        private final String text;
        private Memento(String text) { this.text = text; }
    }
    private String text = "";
    void type(String s) { text += s; }
    Memento save() { return new Memento(text); }
    void restore(Memento m) { text = java.util.Objects.requireNonNull(m).text; }
    public String toString() { return text; }
}

class MementoDemo {
    public static void main(String[] args) {
        Doc d = new Doc();
        d.type("Hello");
        Doc.Memento snap = d.save();
        d.type(" World");
        System.out.println(d); // Hello World
        d.restore(snap);
        System.out.println(d); // Hello
    }
}
```

**Pitfall:** Package-private state is visible to every class in the package and is not an opaque snapshot. Here the nested snapshot's fields and constructor are private; the owning class can access them while the caretaker only retains the handle. Immutable String content can be shared, but retained snapshots still keep old text alive. Large histories may benefit from deltas or persistent structures. This API allows restoring a snapshot into any Doc; add origin validation if cross-document restoration must be forbidden.

---

## 20. Observer

**Intent:** A subject notifies registered observers of events or changes. This demo is synchronous in-process notification; broker-based publish/subscribe has additional delivery and lifecycle semantics.

**When:** UI listeners, event buses, reactive streams, cache invalidation.

```java
interface Observer { void onEvent(String e); }
final class EventBus {
    private final java.util.List<Observer> obs = new java.util.ArrayList<Observer>();
    void subscribe(Observer o) { obs.add(java.util.Objects.requireNonNull(o)); }
    void unsubscribe(Observer o) { obs.remove(o); }
    void publish(String e) {
        // Single-threaded snapshot: callbacks may unsubscribe without invalidating this loop.
        for (Observer o : new java.util.ArrayList<Observer>(obs)) o.onEvent(e);
    }
}

class ObserverDemo {
    public static void main(String[] args) {
        EventBus bus = new EventBus();
        bus.subscribe(new Observer() {
            public void onEvent(String e) { System.out.println("audit " + e); }
        });
        bus.subscribe(new Observer() {
            public void onEvent(String e) { System.out.println("metrics " + e); }
        });
        bus.publish("login");
    }
}
```

**Pitfall:** The snapshot does not make concurrent subscribe/publish safe. A listener removed during a callback remains in that event's snapshot; a new listener starts on the next publish. This demo propagates callback exceptions and stops delivery; choose an explicit isolation/error policy if all listeners must run. Avoid external callbacks under locks and retained unused subscribers. `Observable` was deprecated in Java 9. A distributed event bus additionally needs ordering, retry, idempotency, and backpressure decisions; none are supplied by this list of observers.

---

## 21. State

**Intent:** Object behavior changes with internal state; state objects replace `if (status==)`.

**When:** TCP connection, order lifecycle, media player, vending machine.

```java
interface OrderState {
    OrderState pay();
    OrderState ship();
    String name();
}
final class Created implements OrderState {
    public OrderState pay() { return new Paid(); }
    public OrderState ship() { throw new IllegalStateException("pay first"); }
    public String name() { return "CREATED"; }
}
final class Paid implements OrderState {
    public OrderState pay() { throw new IllegalStateException("already paid"); }
    public OrderState ship() { return new Shipped(); }
    public String name() { return "PAID"; }
}
final class Shipped implements OrderState {
    public OrderState pay() { return this; }
    public OrderState ship() { return this; }
    public String name() { return "SHIPPED"; }
}
final class Order {
    private OrderState state = new Created();
    void pay() { state = state.pay(); }
    void ship() { state = state.ship(); }
    public String toString() { return state.name(); }
}

class StateDemo {
    public static void main(String[] args) {
        Order o = new Order();
        o.pay();
        o.ship();
        System.out.println(o); // SHIPPED
    }
}
```

**Pitfall:** State selects behavior according to lifecycle; Strategy encapsulates an interchangeable policy or algorithm. Strategies may be stateful. The repeated-action policy here is deliberate: paying twice while PAID throws; repeated operations after SHIPPED are no-ops. Change that transition contract explicitly if the domain requires uniform idempotency. Concurrent transitions require coordination beyond this single-threaded example.

---

## 22. Strategy

**Intent:** Swap algorithms behind one interface. Open/closed for behavior.

**When:** Sort comparators, pricing, auth methods, compression, retry policies.

```java
interface Pricing { int price(int cents); }
final class FullPrice implements Pricing {
    public int price(int c) {
        if (c < 0) throw new IllegalArgumentException("negative cents");
        return c;
    }
}
final class PercentOff implements Pricing {
    private final int pct;
    PercentOff(int pct) {
        if (pct < 0 || pct > 100) throw new IllegalArgumentException("percentage outside 0..100");
        this.pct = pct;
    }
    public int price(int c) {
        if (c < 0) throw new IllegalArgumentException("negative cents");
        return (int) ((long) c * (100 - pct) / 100); // floor final nonnegative cents
    }
}
final class Cart {
    private Pricing pricing = new FullPrice();
    void setPricing(Pricing p) { this.pricing = java.util.Objects.requireNonNull(p); }
    int checkout(int cents) { return pricing.price(cents); }
}

class StrategyDemo {
    public static void main(String[] args) {
        Cart cart = new Cart();
        System.out.println(cart.checkout(1000)); // 1000
        cart.setPricing(new PercentOff(20));
        System.out.println(cart.checkout(1000)); // 800
    }
}
```

**Pitfall:** Strategy vs Template Method: Strategy uses composition (plug algorithm); Template Method uses inheritance (override a step). `Comparator` is Strategy. Lambdas in Java 8 are lightweight strategies.

The pricing contract accepts nonnegative int cents, discounts 0–100%, and rounds the resulting price down to a whole cent. Casting before multiplication prevents int overflow; a real pricing domain must specify its own rounding policy.

---

## 23. Template Method

**Intent:** Algorithm skeleton in a base class; subclasses fill in steps.

**When:** Shared workflow, varying steps: parse → validate → persist.

```java
abstract class DataJob {
    final void run() {              // template — final so order cannot change
        extract();
        transform();
        load();
    }
    abstract void extract();
    abstract void transform();
    void load() { System.out.println("load warehouse"); } // default step
}
final class CsvJob extends DataJob {
    void extract() { System.out.println("read csv"); }
    void transform() { System.out.println("normalize rows"); }
}

class TemplateDemo {
    public static void main(String[] args) {
        new CsvJob().run();
    }
}
```

**Pitfall:** This GoF form fixes the workflow in a superclass and customizes steps through overrides. Prefer composition when steps should vary independently at runtime. Spring `JdbcTemplate` centralizes JDBC workflow through callbacks and is normally used without subclassing, so it is not a direct example of this inheritance-based customization. [Spring JdbcTemplate documentation](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/jdbc/core/JdbcTemplate.html)

---

## 24. Visitor

**Intent:** Add operations to an object structure already equipped with `accept`/`visit`, without modifying element classes for every operation. Emulates double dispatch.

**When:** Compilers (type-check, emit, pretty-print AST), document export HTML/PDF, you *cannot* keep adding methods on nodes.

```java
interface Visitor {
    void visit(Lit n);
    void visit(AddNode n);
}
interface Node { void accept(Visitor v); int eval(); }

final class Lit implements Node {
    final int v;
    Lit(int v) { this.v = v; }
    public void accept(Visitor v) { v.visit(this); }
    public int eval() { return v; }
}
final class AddNode implements Node {
    final Node l, r;
    AddNode(Node l, Node r) { this.l = l; this.r = r; }
    public void accept(Visitor v) { v.visit(this); }
    public int eval() { return l.eval() + r.eval(); }
}
final class PrintVisitor implements Visitor {
    public void visit(Lit n) { System.out.print(n.v); }
    public void visit(AddNode n) {
        System.out.print("(");
        n.l.accept(this);
        System.out.print("+");
        n.r.accept(this);
        System.out.print(")");
    }
}

class VisitorDemo {
    public static void main(String[] args) {
        Node ast = new AddNode(new Lit(1), new AddNode(new Lit(2), new Lit(3)));
        ast.accept(new PrintVisitor()); // (1+(2+3))
        System.out.println(" = " + ast.eval());
    }
}
```

**Pitfall:** Adding a **new node type** forces every visitor to change (opposite of Composite+methods). Use Visitor when the *element set is stable* and *operations grow*. Java has no multiple dispatch; `accept`/`visit` fakes it.

---

## 25. Null Object

**Intent:** Replace `null` with an object that does nothing, so clients skip null checks.

```java
interface Logger { void info(String m); }
final class ConsoleLogger implements Logger {
    public void info(String m) { System.out.println(m); }
}
final class SilentLogger implements Logger {
    public void info(String m) { /* no-op */ }
}
final class Service {
    private final Logger log;
    Service(Logger log) { this.log = log; }
    void work() { log.info("working"); }
}

class NullObjectDemo {
    public static void main(String[] args) {
        new Service(new ConsoleLogger()).work();
        new Service(new SilentLogger()).work(); // no NPE, no output
    }
}
```

**Pitfall:** Hides bugs if “missing” should be loud. `Optional` is often clearer for values; Null Object is for *behavior*.

---

## 26. DAO / Repository

**Intent:** Isolate persistence. Domain does not know SQL / Bigtable / I/O.

**When:** Isolating persistence improves domain boundaries or testability. A Repository commonly presents domain aggregates as a collection; a DAO encapsulates persistence access and is not necessarily one object per table.

```java
final class User {
    final String id, email;
    User(String id, String email) { this.id = id; this.email = email; }
}
interface UserRepository {
    void save(User u);
    User findById(String id); // null if absent in this minimal API; Optional is another choice
}
final class InMemoryUserRepository implements UserRepository {
    private final java.util.Map<String, User> db = new java.util.HashMap<String, User>();
    public void save(User u) { db.put(u.id, u); }
    public User findById(String id) { return db.get(id); }
}

class DaoDemo {
    public static void main(String[] args) {
        UserRepository repo = new InMemoryUserRepository();
        repo.save(new User("1", "a@x.com"));
        System.out.println(repo.findById("1").email);
    }
}
```

**Pitfall:** Generic `Repository<T>` that leaks SQL criteria into the domain. One repository per aggregate, not per table, if you are doing DDD.

---

## 27. Dependency Injection

**Intent:** Don’t `new` your dependencies inside the class; receive them (constructor).

**When:** External collaborators, configuration, or nondeterministic services need to be explicit or replaceable in tests. Creating local value objects with `new` is still appropriate. DI is not a GoF pattern or a level-specific requirement. [Dependency injection and service locator](https://martinfowler.com/articles/injection.html)

```java
interface Clock { long now(); }
final class Billing {
    private final Clock clock;
    Billing(Clock clock) { this.clock = clock; }  // injected
    boolean overdue(long dueEpochMs) { return clock.now() > dueEpochMs; }
}

class DiDemo {
    public static void main(String[] args) {
        Billing real = new Billing(new Clock() {
            public long now() { return System.currentTimeMillis(); }
        });
        Billing test = new Billing(new Clock() {
            public long now() { return 100L; }
        });
        System.out.println(test.overdue(50));  // true, deterministic
        System.out.println(real.overdue(0));
    }
}
```

**Pitfall:** Field injection (Spring `@Autowired` on fields) hides required deps. Prefer constructors. Service Locator (below) is the opposite — pull from a bag.

---

## 28. MVC

**Intent:** Split Model (data), View (render), Controller (input → model updates).

**When:** UI and many web frameworks. In a 45-min design, say the split; don’t draw Spring annotations.

```java
final class CounterModel {
    private int n;
    int get() { return n; }
    void inc() { n++; }
}
final class CounterView {
    void render(int n) { System.out.println("count=" + n); }
}
final class CounterController {
    private final CounterModel model;
    private final CounterView view;
    CounterController(CounterModel m, CounterView v) { model = m; view = v; }
    void onClick() { model.inc(); view.render(model.get()); }
}

class MvcDemo {
    public static void main(String[] args) {
        CounterController c = new CounterController(new CounterModel(), new CounterView());
        c.onClick();
        c.onClick();
    }
}
```

**Pitfall:** Fat controllers. Business rules live in the model/domain, not the HTTP layer.

---

## 29. Producer–Consumer

**Intent:** Decouple producers and consumers with a queue. Bound memory, absorb bursts.

**When:** Pipelines, log shippers, work queues. Java: `BlockingQueue`.

```java
class ProducerConsumerDemo {
    public static void main(String[] args) throws InterruptedException, java.util.concurrent.ExecutionException {
        final java.util.concurrent.BlockingQueue<Integer> q =
                new java.util.concurrent.ArrayBlockingQueue<Integer>(2);
        java.util.concurrent.ExecutorService workers = java.util.concurrent.Executors.newFixedThreadPool(2);
        java.util.concurrent.CompletionService<Void> completed =
                new java.util.concurrent.ExecutorCompletionService<Void>(workers);
        try {
            completed.submit(() -> {
                for (int i = 0; i < 5; i++) q.put(i);
                q.put(-1); // reserved sentinel; exactly one consumer
                return null;
            });
            completed.submit(() -> {
                while (true) {
                    int value = q.take();
                    if (value == -1) return null;
                    System.out.println("got " + value);
                }
            });
            // Observe whichever task completes/fails first, not a fixed join order.
            for (int i = 0; i < 2; i++) completed.take().get();
        } finally {
            workers.shutdownNow(); // interrupts a peer blocked in put/take on failure/cancellation
        }
    }
}
```

**Pitfall:** An effectively unbounded queue can exhaust memory when producers outpace consumers; this bounded queue blocks producers. The demo has one producer/consumer and reserves -1 as a terminator. Multiple consumers need a compatible shutdown protocol, such as one terminal message per consumer after production ends. CompletionService observes either task's failure so cleanup can interrupt the peer instead of leaving it blocked forever. BlockingQueue has no intrinsic close operation, and executor shutdown alone does not signal queue end-of-stream. Competing consumers remove individual work items; publish/subscribe fan-out is a different delivery model. [BlockingQueue lifecycle and operations](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/BlockingQueue.html)

---

## 30. Immutable object

**Intent:** An object's observable state does not change after construction. Deep immutability and safe construction/publication allow safe sharing; `final` references alone do not freeze referenced mutable objects.

**When:** Value objects, map keys, messages on a queue.

```java
final class Money {
    private final String currency;
    private final long cents;
    Money(String currency, long cents) {
        if (currency == null) throw new IllegalArgumentException();
        this.currency = currency;
        this.cents = cents;
    }
    String currency() { return currency; }
    long cents() { return cents; }
    Money plus(Money o) {
        java.util.Objects.requireNonNull(o);
        if (!currency.equals(o.currency)) throw new IllegalArgumentException("fx");
        return new Money(currency, Math.addExact(cents, o.cents)); // reject long overflow
    }
    @Override public boolean equals(Object other) {
        if (this == other) return true;
        if (!(other instanceof Money)) return false;
        Money money = (Money) other;
        return cents == money.cents && currency.equals(money.currency);
    }
    @Override public int hashCode() {
        return 31 * currency.hashCode() + Long.hashCode(cents);
    }
}

class ImmutableDemo {
    public static void main(String[] args) {
        Money a = new Money("USD", 100);
        Money b = a.plus(new Money("USD", 50));
        System.out.println(a.cents() + " then " + b.cents()); // 100 then 150
    }
}
```

**Pitfall:** A mutable collection needs an independent unmodifiable copy, plus immutable/copied elements when deep immutability is required. A value object also needs consistent `equals`/`hashCode` if value equality is intended. Here cents may be negative; currencies must match exactly, and overflow raises `ArithmeticException` rather than wrapping. This simplified cents model does not implement currency conversion or variable minor-unit scales. [Checked arithmetic](https://docs.oracle.com/javase/8/docs/api/java/lang/Math.html#addExact-long-long-)

---

## 31. Marker interface

**Intent:** Interface with no methods; tags a type for runtime/JVM behavior.

**When:** A property should be represented in the Java type system, as with `Serializable` or `RandomAccess`. Annotations suit metadata; marker interfaces additionally allow compile-time parameter and generic-bound restrictions.

```java
interface Auditable {} // marker
final class Payment implements Auditable {
    final long id;
    Payment(long id) { this.id = id; }
}

class MarkerDemo {
    static void audit(Object o) {
        if (o instanceof Auditable) System.out.println("audit " + o.getClass().getSimpleName());
        else System.out.println("skip");
    }
    public static void main(String[] args) {
        audit(new Payment(1));
        audit("nope");
    }
}
```

**Pitfall:** `Cloneable` does not declare `clone()`, so it is not a useful generic copying API. Choose a marker interface when APIs should accept only the marked type, for example `audit(Auditable value)`, and an annotation when metadata/configuration is the goal. Neither automatically supplies behavior; code or a framework must interpret it.

---

## 32. Front Controller

**Intent:** Single entry that routes all requests (HTTP servlet, API gateway handler).

**When:** Web apps, one `doGet` that dispatches by path.

```java
interface Action { void exec(String body); }
final class FrontController {
    private final java.util.Map<String, Action> routes = new java.util.HashMap<String, Action>();
    FrontController register(String path, Action a) { routes.put(path, a); return this; }
    void handle(String path, String body) {
        Action a = routes.get(path);
        if (a == null) { System.out.println("404 " + path); return; }
        a.exec(body);
    }
}

class FrontControllerDemo {
    public static void main(String[] args) {
        new FrontController()
                .register("/health", new Action() { public void exec(String b) { System.out.println("ok"); } })
                .register("/echo", new Action() { public void exec(String b) { System.out.println(b); } })
                .handle("/echo", "hi");
    }
}
```

**Pitfall:** One class routing *and* doing business logic. Controller routes; domain executes.

---

## 33. Service Locator

**Intent:** Consumers look up dependencies from a registry instead of receiving them explicitly. The registry need not be global, though this example is.

**When:** Some legacy integration or infrastructure lookup boundaries use it. Prefer explicit injection for ordinary application collaborators; evaluate the tradeoff rather than treating every registry as forbidden.

```java
final class ServiceLocator {
    private static final java.util.Map<Class<?>, Object> REG = new java.util.HashMap<Class<?>, Object>();
    static synchronized <T> void put(Class<T> type, T impl) {
        REG.put(java.util.Objects.requireNonNull(type), java.util.Objects.requireNonNull(type.cast(impl)));
    }
    static synchronized <T> T get(Class<T> type) {
        Object value = REG.get(java.util.Objects.requireNonNull(type));
        if (value == null) throw new IllegalStateException("unregistered: " + type.getName());
        return type.cast(value);
    }
}

class ServiceLocatorDemo {
    public static void main(String[] args) {
        ServiceLocator.put(Runnable.class, new Runnable() {
            public void run() { System.out.println("from locator"); }
        });
        ServiceLocator.get(Runnable.class).run();
    }
}
```

**Pitfall:** Synchronizing registry access does not make returned services thread-safe. Global lookup can obscure required dependencies and complicate lifecycle/testing. Injection and lookup can coexist at infrastructure boundaries; a composition root can retrieve/configure objects and inject them into application code. Do not equate all of Spring with this minimal registry.

---

## When which pattern

| You notice… | Reach for |
|---|---|
| Product chosen by a discriminator | Simple factory / registry |
| Subclass should choose a workflow's product | Factory Method |
| Products must match as a family | Abstract Factory |
| 6 constructor args, 4 optional | Builder |
| “Copy this configured object” | Prototype (copy ctor) |
| One shared instance per defining class loader | Enum/holder singleton, or inject a scoped instance |
| Legacy API doesn’t match yours | Adapter |
| Two independent axes of variation | Bridge |
| Tree of parts, same operations | Composite |
| Wrap streams / add logging without subclass | Decorator |
| Hide 5 classes behind `checkout()` | Facade |
| 10^7 almost-identical objects | Flyweight |
| Lazy / remote / access control, same interface | Proxy |
| Filters, approvals | Chain |
| Undo, queue jobs | Command |
| Tiny grammar | Interpreter |
| `for (x : collection)` | Iterator |
| Widgets all call each other | Mediator |
| Snapshot / restore | Memento |
| Many listeners | Observer |
| Lifecycle `if (state==)` | State |
| Swap algorithm | Strategy |
| Shared steps, varying hooks | Template Method |
| Many ops on a stable AST | Visitor |
| `if (x != null) x.f()` everywhere | Null Object or `Optional` |
| SQL in the service class | Repository / DAO |
| Hidden external collaborators in business logic | Constructor DI; local value-object construction is fine |
| Burst traffic, slow I/O | Producer–Consumer + bounded queue |

---

## Interview one-liners (L4/L5)

- **Strategy vs State:** Strategy is *how*; State is *where in the lifecycle*.
- **Decorator vs Proxy vs Adapter:** same interface + add behavior / same interface + control access / **different** interface.
- **Facade vs Mediator:** facade is one-way simplify for clients; mediator is many colleagues collaborating.
- **Factory vs DI:** factory *creates*; DI *receives*. Spring is both (container factories + constructor injection).
- **Singleton:** say enum, say it hurts tests, offer to pass the dependency instead.
- **Template vs Strategy:** inheritance vs composition. Prefer composition unless the skeleton is truly fixed.
- **Observer vs brokered pub/sub:** local callbacks do not provide durable delivery or retries. For a distributed design, explicitly choose ordering, delivery, and backpressure semantics.

---

## What not to memorize

UML diagrams of all 23. Spring stereotype annotations as if they were patterns. Implementing Interpreter for SQL. Flyweight for 20 objects. Singleton for a `UserService`.
