/**
 * Placeholder rendered at build time and during hydration, before the study state
 * loads. It is a <section>, not a <div>, so Preact replaces it rather than patching
 * the page element (hydration keeps attributes such as aria-busy otherwise).
 */
export function Loading() {
  return <section class="page-loading" aria-busy="true" aria-label="Loading" />;
}
