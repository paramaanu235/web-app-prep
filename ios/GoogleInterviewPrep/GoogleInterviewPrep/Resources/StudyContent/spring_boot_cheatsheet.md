# Spring Boot & Spring Framework cheat sheet

**Pinned (Aug 2026):** Spring Boot **4.1.1** · Spring Framework **7.0.9** · Spring Security **7.1.1** · Spring Data BOM **2026.0.1**

These are separate reference fragments, not a complete application to concatenate. Java imports and application-specific domain methods are omitted where obvious; `...` denotes pseudocode. Use Boot's dependency management instead of independently pinning the component versions below.

| Piece | Version in Boot 4.1.1 |
|---|---|
| Spring Framework | 7.0.9 |
| Spring Security | 7.1.1 |
| Spring Data | 2026.0.1 |
| Hibernate ORM | 7.4.x |
| Jackson | **3.x** (also manages 2.x BOM) |
| Tomcat | 11.0.x |
| Micrometer | 1.17.x |
| Reactor | 2025.0.x |
| Java | **17 minimum, 21 strongly recommended** |
| JUnit Jupiter | **6.0.x** (still uses `org.junit.jupiter` packages) |

**Boot 4 naming:** `spring-boot-starter-web` is **deprecated**. Use **`spring-boot-starter-webmvc`** (servlet) or **`spring-boot-starter-webflux`** (reactive).

Jakarta EE APIs use `jakarta.*` (e.g. persistence, servlet, validation). Java SE packages such as `javax.sql` and `javax.crypto` retain their names. Framework nullness metadata uses JSpecify; it does not replace runtime validation.

---

## 1. Boot vs Framework

| | Spring Framework | Spring Boot |
|---|---|---|
| What | DI, MVC, TX, AOP, Data access | Opinionated runtime on top of Framework |
| You write | `@Component`, `@Transactional`, `DispatcherServlet` XML in 2008… | `@SpringBootApplication`, starters, auto-config |
| Config | You wire it | Classpath + `application.yml` + auto-config |
| Embedded server | You set up Tomcat | Starter brings Tomcat/Jetty/Netty |

Interview line: “Boot auto-configures Framework when the right starter is on the classpath. I can exclude or replace any auto-config.”

---

## 2. New project (Maven)

```xml
<!-- Fragment inside <project>; keep generated coordinates/modelVersion/build. -->
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>4.1.1</version>
</parent>
<properties>
  <java.version>21</java.version>
</properties>
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-oauth2-resource-server</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
  </dependency>
  <dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc-test</artifactId>
    <scope>test</scope>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa-test</artifactId>
    <scope>test</scope>
  </dependency>
  <dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-test</artifactId>
    <scope>test</scope>
  </dependency>
</dependencies>
```

Gradle: `id 'org.springframework.boot' version '4.1.1'` plus dependency management (the dependency-management plugin or Boot BOM). The Maven fragment also needs `spring-boot-maven-plugin` in `<build><plugins>` to package/run an executable Boot jar. Generate the full project with Spring Initializr.

Add the Flyway starter and `org.flywaydb:flyway-database-postgresql` if choosing Flyway, and `io.micrometer:micrometer-registry-prometheus` for the Prometheus endpoint. Test database choices are explained in section 13.

```java
@SpringBootApplication
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }
}
```

`@SpringBootApplication` = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan` (this package and below).

---

## 3. application.yml

```yaml
spring:
  application:
    name: orders
  threads:
    virtual:
      enabled: true          # Java 21 virtual threads for Tomcat/request
  datasource:
    url: jdbc:postgresql://localhost:5432/orders
    username: app
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
  jpa:
    open-in-view: false      # NEVER leave true in APIs
    hibernate:
      ddl-auto: validate     # prod: validate/none; Flyway/Liquibase owns schema
    properties:
      hibernate:
        jdbc:
          time_zone: UTC
  jackson:
    default-property-inclusion: non_null

server:
  port: 8080
  shutdown: graceful
  tomcat:
    threads:
      max: 200               # platform-thread pool only; no effect with virtual threads

management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
  endpoint:
    health:
      probes:
        enabled: true        # /actuator/health/liveness + readiness

logging:
  level:
    org.springframework.web: INFO
    org.hibernate.SQL: WARN
```

Profiles: `application-prod.yml` + `spring.profiles.active=prod`.

`@ConfigurationProperties(prefix = "app.orders")` + `@EnableConfigurationProperties` or `@ConfigurationPropertiesScan`. Prefer this over a pile of `@Value`.

---

## 4. DI (Framework core)

```java
@Service
public class OrderService {
    private final OrderRepository repo;
    private final Clock clock;

    public OrderService(OrderRepository repo, Clock clock) {
        this.repo = repo;
        this.clock = clock;
    }

    @Transactional
    public Order pay(long id) {
        Order o = repo.findById(id).orElseThrow(() -> new NotFound(id));
        o.pay(clock.instant());
        return o;
    }
}

@Configuration
class TimeConfig {
    @Bean Clock clock() { return Clock.systemUTC(); }
}
```

- Prefer constructor injection for required dependencies and easy unit tests. A sole constructor needs no `@Autowired`; Lombok is optional, not required.
- Default singleton. `@Scope("prototype")` rare. `@RequestScope` for request-bound state.
- `@Primary` / `@Qualifier("jpa")` when multiple beans of one type.
- `@ConditionalOn*` — how Boot auto-config works; you can write your own.
- Circular deps: don’t. In Boot 2.6+ they’re an error unless you opt in (don’t).

Lifecycle: `@PostConstruct` / `InitializingBean` / `ApplicationRunner` / `CommandLineRunner`. Prefer `ApplicationRunner` for startup jobs.

AOP in the default proxy mode: **self-invocation does not go through the proxy** (`this.pay()` cannot start the annotated transaction; an already active transaction still applies). Extract a second bean or use `TransactionTemplate` for programmatic transactions. `@Async` also requires `@EnableAsync`; singleton scope does not make mutable fields thread-safe.

---

## 5. Web MVC (servlet stack)

```java
@RestController
@RequestMapping("/api/orders")
class OrderController {
    private final OrderService service;

    OrderController(OrderService service) { this.service = service; }

    @GetMapping("/{id}")
    OrderResponse get(@PathVariable long id) {
        return OrderResponse.from(service.get(id));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    OrderResponse create(@Valid @RequestBody CreateOrderRequest req) {
        return OrderResponse.from(service.create(req));
    }

    @GetMapping
    Page<OrderResponse> list(
            @RequestParam(defaultValue = "0") @Min(0) int page,
            @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size) {
        return service.list(PageRequest.of(page, size)).map(OrderResponse::from);
    }
}

record CreateOrderRequest(@NotNull @Positive Long userId, @NotNull @Positive BigDecimal total) {}
record OrderResponse(long id, String status, BigDecimal total) {
    static OrderResponse from(Order o) {
        return new OrderResponse(o.getId(), o.getStatus().name(), o.getTotal());
    }
}
```

**Records as DTOs** are first-class on Boot 3+/4.

Exception handling:

```java
@RestControllerAdvice
class ApiErrors {
    @ExceptionHandler(NotFound.class)
    ProblemDetail notFound(NotFound ex) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, "Order not found");
    }

    @ExceptionHandler({MethodArgumentNotValidException.class, HandlerMethodValidationException.class})
    ProblemDetail invalid(Exception ex) {
        HttpStatus status = ex instanceof HandlerMethodValidationException validation
                && validation.isForReturnValue()
                ? HttpStatus.INTERNAL_SERVER_ERROR : HttpStatus.BAD_REQUEST;
        return ProblemDetail.forStatusAndDetail(status, "Validation failed");
    }
}
```

`ProblemDetail` (Framework 6+) implements problem details, now specified by RFC 9457 (superseding RFC 7807). Return-value validation errors are server errors; invalid request input is a client error.

Filters vs interceptors vs MVC advice:
- **Filter** — servlet, before DispatcherServlet (CORS, tracing)
- **HandlerInterceptor** — MVC, has `HandlerMethod`
- **`@ControllerAdvice`** — exceptions / `@InitBinder` / `@ModelAttribute`

---

## 6. Validation

Jakarta Validation (`jakarta.validation`):

```java
public record UserIn(
    @Email @NotBlank String email,
    @NotNull @Size(min = 8) String password
) {}
```

`@Valid` cascades into nested objects; add `@NotNull` when the object must exist. Many constraints (`@Positive`, `@Size`, `@Email`) accept null by themselves. MVC 6.1+ has built-in method validation: remove class-level `@Validated` on controllers to use it. Service-layer method validation uses `@Validated` and a proxy; an interface is not required.

---

## 7. Spring Data JPA

```java
@Entity
@Table(name = "orders")
class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Version
    private Long version;        // optimistic conflict detection

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private User user;

    @Enumerated(EnumType.STRING)
    private Status status;

    private BigDecimal total;

    protected Order() {}          // JPA
    // getters, domain methods
}

interface OrderRepository extends JpaRepository<Order, Long> {
    @Query("select o from Order o join fetch o.user where o.id = :id")
    Optional<Order> findWithUser(@Param("id") long id);

    Page<Order> findByUserId(long userId, Pageable pageable);

    @Transactional
    @Modifying(flushAutomatically = true, clearAutomatically = true)
    @Query("update Order o set o.status = :s where o.id = :id")
    int updateStatus(@Param("id") long id, @Param("s") Status s);
}
```

**N+1:** fetch joins or `@EntityGraph` for the relations the response needs. With `open-in-view: false`, fetch and map DTOs inside the service transaction; returning an entity with uninitialized lazy relations can fail during serialization. Avoid paginating collection fetch joins; page IDs first, then fetch the related data. Bulk JPQL updates bypass entity callbacks and automatic `@Version` checks; use managed updates or an explicit version predicate/increment when conflict detection matters.

Transactions:

```java
@Transactional                 // proxy, rollback on RuntimeException
public void pay(long id) { ... }

@Transactional(readOnly = true)
public Order get(long id) { ... }

@Transactional(propagation = Propagation.REQUIRES_NEW)
public void audit() { ... }
```

By default unchecked exceptions and `Error` trigger rollback; checked exceptions require a matching rollback rule (e.g. `rollbackFor = Exception.class`) or an explicit global override. `readOnly=true` is an optimization hint, not a write prohibition. `REQUIRES_NEW` uses an independent transaction and can require an extra pooled connection.

Schema: **Flyway** (`db/migration/V1__init.sql`) or Liquibase. `ddl-auto=update` is not a migration strategy.

---

## 8. Spring Security 7 (filter chain)

```java
import static org.springframework.security.config.http.SessionCreationPolicy.STATELESS;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
class SecurityConfig {

    @Bean
    SecurityFilterChain api(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())          // stateless JWT API; keep CSRF for cookie sessions
            .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
            .authorizeHttpRequests(a -> a
                .requestMatchers("/actuator/health/**", "/api/public/**").permitAll()
                .requestMatchers(HttpMethod.POST, "/api/orders/**").hasAuthority("SCOPE_orders:write")
                .anyRequest().authenticated())
            .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
            .build();
    }
}
```

Method security:

```java
@PreAuthorize("hasAuthority('SCOPE_orders:write')")
public Order create(...) { ... }

@PreAuthorize("#subject == authentication.name")
public List<Order> bySubject(String subject) { ... }
```

Password: `PasswordEncoder` bean = `BCryptPasswordEncoder` (or Argon2). Never `NoOp`.

Default JWT scopes map to `SCOPE_...` authorities. The principal is a `Jwt`, not your domain `User`; `authentication.name` normally uses `sub`. Map that subject to a local account and enforce order ownership in the service/repository. Do not trust a request's `userId` as authorization. The sample disables CSRF only for bearer tokens explicitly sent in the Authorization header; stateless cookie auth can still be vulnerable to CSRF.

Resource server yml:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/app
          audiences: orders-api   # match the audience issued for this API
```

CORS: `CorsConfigurationSource` bean or `http.cors(...)`. Don’t `*` + credentials.

---

## 9. WebFlux (when you actually need it)

Use WebFlux for: many concurrent I/O waits, streaming, gateway. Don’t mix blocking JPA on the event loop.

```java
@RestController
class ReactiveOrderController {
    private final OrderR2dbcRepo repo;

    ReactiveOrderController(OrderR2dbcRepo repo) { this.repo = repo; }

    @GetMapping("/{id}")
    Mono<Order> get(@PathVariable long id) {
        return repo.findById(id).switchIfEmpty(Mono.error(
            new ResponseStatusException(HttpStatus.NOT_FOUND)));
    }

    @GetMapping
    Flux<Order> all() {
        return repo.findAll();
    }
}
```

`spring-boot-starter-webflux` + Netty. **Don’t** put both webmvc and webflux starters unless you know which is the web application type (`spring.main.web-application-type`).

---

## 10. Virtual threads (Java 21 + Boot 3.2 / 4.x)

```yaml
spring.threads.virtual.enabled: true
```

Boot can use virtual threads for supported servlet handling and auto-configured task execution; a custom executor can change this. On Java 21–23, blocking while holding a monitor can pin a carrier; Java 24's JEP 491 removes monitor-related pinning. Do not mechanically replace every `synchronized` with `ReentrantLock`. JDBC still consumes a bounded DB connection; virtual threads improve I/O concurrency, not CPU speed or database capacity. Consider `spring.main.keep-alive=true` for applications relying on daemon virtual threads without another non-daemon thread keeping the JVM alive.

---

## 11. Actuator & observability

- Liveness: application state requiring a restart; keep shared DB/broker failures out to avoid restart storms
- Readiness: whether this instance should receive traffic. Boot does not add DB/broker checks to readiness automatically; decide which dependencies to include, because a shared outage can make every replica unready
- Metrics: Micrometer → Prometheus (`/actuator/prometheus`, needs its registry dependency)
- Tracing: Micrometer Tracing + OTLP; add `spring-boot-starter-opentelemetry` (configuration alone does not install it)
- Never expose `env`, `beans`, `heapdump` without auth

```yaml
management:
  tracing:
    sampling:
      probability: 0.1
  opentelemetry:
    tracing:
      export:
        otlp:
          endpoint: http://otel-collector:4318/v1/traces
```

This OTLP property path is for Boot 4; the Boot 3 `management.otlp.tracing.*` path should not be copied into this baseline. See [Boot tracing configuration](https://docs.spring.io/spring-boot/reference/actuator/tracing.html).

---

## 12. Config, secrets, profiles

Precedence (high wins): command line → env (`SPRING_DATASOURCE_URL`) → `application-{profile}.yml` → `application.yml`.

```java
@ConfigurationProperties(prefix = "app")
record AppProps(int pageSize, URI billingBase) {}
```

Bind maps/lists. In environment variables, replace dots with underscores, remove dashes, then uppercase: `app.page-size` → `APP_PAGESIZE` (not `APP_PAGE_SIZE`).

---

## 13. Testing

```java
@SpringBootTest
@AutoConfigureMockMvc
class OrderIT {
    @Autowired MockMvc mvc;
    @MockitoBean OrderRepository repo;   // Boot 3.4+/4: @MockitoBean not @MockBean

    @Test
    void getOrder() throws Exception {
        when(repo.findById(1L)).thenReturn(Optional.of(order));
        mvc.perform(get("/api/orders/1").with(jwt().jwt(j -> j.subject("u"))))
           .andExpect(status().isOk())
           .andExpect(jsonPath("$.id").value(1));
    }
}

@DataJpaTest
class OrderRepoTest {
    @Autowired OrderRepository repo;
    @Test
    void save() { ... }
}

@WebMvcTest(OrderController.class)
class OrderWebTest {
    @Autowired MockMvc mvc;
    @MockitoBean OrderService service;
}
```

Slices: `@WebMvcTest` (web layer), `@DataJpaTest` (repos + embedded/testcontainers DB), `@JsonTest`, `@SpringBootTest` (almost everything).

Testcontainers: `spring-boot-testcontainers` + `@ServiceConnection` on a `@Container PostgreSQLContainer`.

Boot 4 modularized testing: the POM above includes webmvc/data-jpa test starters. Key imports are `org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest`, `org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc`, `org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest`, and `org.springframework.test.context.bean.override.mockito.MockitoBean`. Add an embedded DB test dependency (e.g. H2), or Testcontainers' PostgreSQL and JUnit modules plus `@Testcontainers`; a running container runtime is required. The `order` fixture in `OrderIT` must be created by the test. JWT request helpers bypass token decoding: separately test real JWT validation and authorization, including 401/403 and ownership failures.

---

## 14. Transactions, events, messaging

```java
@Service
class OrderService {
    private final ApplicationEventPublisher events;
    private final OrderRepository repo;

    OrderService(ApplicationEventPublisher events, OrderRepository repo) {
        this.events = events;
        this.repo = repo;
    }

    @Transactional
    public Order pay(long id) {
        Order o = repo.findById(id).orElseThrow(() -> new NotFound(id));
        o.pay();  // domain transition; implement idempotency/payment verification
        events.publishEvent(new OrderPaid(o.getId())); // listener after commit if @TransactionalEventListener
        return o;
    }
}

@Component
class PaidListener {
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void on(OrderPaid e) { /* queue email */ }
}
```

Kafka: `spring-boot-starter-kafka`; Rabbit: `spring-boot-starter-amqp`. After-commit listeners are in-process and are not durable delivery. Writes performed by an after-commit listener need their own transaction; a broker enqueue can still fail after the DB commit. Use a transactional outbox and an idempotent consumer when committed changes must reliably produce messages.

---

## 15. Caching

```java
@EnableCaching
@Configuration
class CacheConfig {
    @Bean
    CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("orders"); // local demo: no eviction/TTL
    }
}

@Cacheable("orders")
public Order get(long id) { ... }

@CacheEvict(value = "orders", key = "#result.id", condition = "#result != null")
public Order save(Order order) { ... }
```

This assumes `save` returns the persisted object with its generated ID. Prefer immutable cached DTOs. Use a bounded provider (e.g. Caffeine) or Redis with an explicit TTL/invalidation policy; a remote cache is not mandatory. Coordinate eviction with transaction commit so a rollback or concurrent read cannot leave stale state.

---

## 16. Boot 3 → 4 / Framework 6 → 7 deltas worth saying

- Java EE `javax.*` → `jakarta.*` (done in Boot 3; Java SE `javax.*` stays)
- `spring-boot-starter-web` → **`spring-boot-starter-webmvc`**
- Jackson **3** default in Boot 4 (APIs shifted; `JsonMapper`)
- Hibernate **7**
- Auto-configuration and testing are more modular; include technology-specific starters
- `@MockBean` → `@MockitoBean`
- Native image / AOT first-class (`spring-boot-starter-parent` + Graal)
- gRPC integration has its own starter/configuration; protocol code generation is a separate build concern
- ProblemDetail, HTTP interface clients (`@HttpExchange`)
- RestClient (6.1+) for new synchronous clients; `RestTemplate` is deprecated in Framework 7

```java
@Bean
RestClient billingClient(RestClient.Builder b) {
    return b.baseUrl("https://billing.internal").build();
}
```

HTTP interface:

Add `spring-boot-starter-restclient` for the auto-configured `RestClient.Builder`. An annotated interface alone is not a Spring bean: register an HTTP service client or construct a proxy with `HttpServiceProxyFactory` and `RestClientAdapter`.

```java
@HttpExchange("/v1/invoices")
interface BillingApi {
    @GetExchange("/{id}")
    Invoice get(@PathVariable long id);
}
```

---

## 17. Concurrency & request path (interview)

```
HTTP → Tomcat VT/platform thread
    → Filters (Security, CORS, tracing)
    → DispatcherServlet
    → Controller
    → Service @Transactional (proxy)
    → Repository (EntityManager / Hikari connection)
```

Connection budget: sum every replica's pool maximum plus migrations, jobs and operational clients; leave headroom under DB `max_connections`. Request threads do not need to equal pool size. Virtual threads can wait for connections, but still need deadlines and admission limits under overload.

Graceful shutdown: `server.shutdown=graceful` + K8s `preStop` + readiness fail first.

---

## 18. Footguns

| Footgun | Fix |
|---|---|
| `spring.jpa.open-in-view=true` | `false`; fetch joins |
| Field injection | constructor |
| `this.method()` skips `@Transactional` | another bean |
| `FetchType.EAGER` everywhere | LAZY + explicit fetch |
| `ddl-auto=update` in prod | Flyway |
| Swallow an exception inside `@Transactional` | Proxy may commit unless marked rollback-only; a DB failure may already mark rollback-only and cause `UnexpectedRollbackException` |
| `RestTemplate` as `new RestTemplate()` | bean + timeouts |
| Unbounded `@Async` concurrency | Bound platform queues or virtual-thread access to scarce resources; choose rejection/backpressure deliberately (`CallerRunsPolicy` runs on the submitter) |
| Expose `/actuator/*` | auth + subset |
| `==` on entities | Define proxy-aware equals/hashCode carefully; two transient null IDs must not imply equality, and generated IDs can destabilize hash collections |
| Bidirectional JSON loop | DTO / `@JsonIgnore` / records |
| CSRF disabled + cookie authentication | CSRF exposure; session fixation is a separate concern |

---

## 19. Component scan of the Spring portfolio (Boot 4.1)

| Starter / project | Use |
|---|---|
| webmvc / webflux | HTTP APIs |
| data-jpa / data-jdbc / data-mongodb / data-redis | persistence |
| security + oauth2-resource-server / oauth2-client | authn/z |
| actuator | ops |
| validation | Bean Validation |
| batch 6.x | jobs |
| kafka / amqp / pulsar | messaging |
| integration 7.x | EIP |
| graphql 2.x | GraphQL |
| session | clustered HTTP sessions |
| flyway / liquibase | migrations |
| test + technology test starters | JUnit Jupiter 6; add slice and Testcontainers dependencies as needed |
| grpc | gRPC (Boot 4) |

---

## 20. One-screen Boot 4 service

```java
@SpringBootApplication
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }
}

@RestController
@RequestMapping("/api/orders")
class OrderController {
    private final OrderRepository repo;
    OrderController(OrderRepository repo) { this.repo = repo; }

    @GetMapping("/{id}")
    Order get(@PathVariable Long id) {
        return repo.findById(id).orElseThrow(() -> new ResponseStatusException(NOT_FOUND));
    }
}

interface OrderRepository extends JpaRepository<Order, Long> {}
```

This is only a routing/persistence skeleton and requires the `Order` entity. Before exposing it, add authentication plus ownership checks, DTO mapping inside service transactions, schema migrations and appropriate operational configuration. These choices depend on requirements, not a fixed interview-level checklist.

---

## Review notes and official references

Reviewed against Boot 4.1 / Framework 7 documentation. Maven XML and all YAML fragments were parsed successfully. Java examples were reviewed as fragments; no complete Spring application was compiled or integration-tested.

- Dependency and test setup: [managed coordinates](https://docs.spring.io/spring-boot/appendix/dependency-versions/coordinates.html), [Boot testing](https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html).
- Authentication and authority mapping: [JWT resource server](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html).
- Request validation and proxy behavior: [MVC validation](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-validation.html), [cache annotations](https://docs.spring.io/spring-framework/reference/integration/cache/annotations.html).
- Virtual-thread version differences: [JDK 24 changes](https://docs.oracle.com/en/java/javase/25/migrate/significant-changes-jdk-24.html). Client configuration: [calling REST services](https://docs.spring.io/spring-boot/reference/io/rest-client.html).
