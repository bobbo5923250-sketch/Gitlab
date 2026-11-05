(function () {
  const d = window.PORTFOLIO;
  const $ = (id) => document.getElementById(id);

  const el = (tag, attrs = {}, children = []) => {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "text") node.textContent = v;
      else node.setAttribute(k, v);
    }
    for (const c of [].concat(children)) if (c) node.append(c);
    return node;
  };

  const chips = (items) =>
    el("ul", { class: "chips" }, items.map((t) => el("li", { class: "chip", text: t })));

  const externalLink = (href, text, cls) =>
    el("a", { href, text, target: "_blank", rel: "noopener noreferrer", ...(cls && { class: cls }) });

  // ---------- Header & hero ----------
  document.title = `${d.name} — ${d.role}`;
  $("brand").textContent = d.name;
  $("hero-role").textContent = `> ${d.role} · ${d.location}`;
  $("hero-name").textContent = d.name;
  $("hero-tagline").textContent = d.tagline;

  const actions = $("hero-actions");
  actions.append(el("a", { class: "btn btn-primary", href: "#projects", text: "View projects" }));
  if (d.resumeUrl) actions.append(externalLink(d.resumeUrl, "Download résumé", "btn"));
  actions.append(el("a", { class: "btn", href: `mailto:${d.email}`, text: "Get in touch" }));

  $("stats").append(
    ...d.stats.map((s) =>
      el("li", {}, [el("strong", { text: s.value }), el("span", { text: s.label })])
    )
  );

  // ---------- About ----------
  $("about-body").append(...d.about.map((p) => el("p", { text: p })));

  // ---------- Skills ----------
  $("skills-grid").append(
    ...d.skills.map((s) => el("div", { class: "card" }, [el("h3", { text: s.group }), chips(s.items)]))
  );

  // ---------- Projects ----------
  const grid = $("projects-grid");
  const filters = $("filters");
  const allTags = ["All", ...new Set(d.projects.flatMap((p) => p.tags))];

  const renderProjects = (tag) => {
    const list = d.projects
      .filter((p) => tag === "All" || p.tags.includes(tag))
      .sort((a, b) => Number(b.featured) - Number(a.featured));

    grid.replaceChildren(
      ...list.map((p) => {
        const links = el("div", { class: "project-links" });
        if (p.repo) links.append(externalLink(p.repo, "Code →"));
        if (p.demo) links.append(externalLink(p.demo, "Live demo →"));

        return el("article", { class: "card project" }, [
          el("div", { class: "project-head" }, [
            el("h3", { text: p.title }),
            p.featured && el("span", { class: "badge mono", text: "featured" }),
          ]),
          el("p", { text: p.summary }),
          p.highlights?.length &&
            el("ul", { class: "highlights" }, p.highlights.map((h) => el("li", { text: h }))),
          chips(p.tags),
          links.childElementCount && links,
        ]);
      })
    );

    for (const b of filters.children) b.setAttribute("aria-selected", String(b.dataset.tag === tag));
  };

  filters.append(
    ...allTags.map((t) => {
      const b = el("button", { class: "filter", role: "tab", "data-tag": t, text: t });
      b.addEventListener("click", () => renderProjects(t));
      return b;
    })
  );
  renderProjects("All");

  // ---------- Experience ----------
  $("timeline").append(
    ...d.experience.map((x) =>
      el("li", {}, [
        el("h3", { text: `${x.role} · ${x.company}` }),
        el("p", { class: "meta mono", text: x.period }),
        el("ul", {}, x.points.map((pt) => el("li", { text: pt }))),
      ])
    )
  );

  $("education").append(
    ...d.education.map((e) =>
      el("li", {}, [el("strong", { text: e.degree }), el("small", { text: `${e.school} · ${e.period}` })])
    )
  );
  $("certifications").append(...d.certifications.map((c) => el("li", { text: c })));

  // ---------- Contact & footer ----------
  const mail = $("contact-email");
  mail.href = `mailto:${d.email}`;
  mail.textContent = d.email;

  $("socials").append(...d.socials.map((s) => el("li", {}, externalLink(s.url, s.label))));
  $("footer-text").textContent = `© ${new Date().getFullYear()} ${d.name}. Built with plain HTML, CSS & JS.`;

  // ---------- Theme toggle ----------
  $("theme-toggle").addEventListener("click", () => {
    const root = document.documentElement;
    const current =
      root.dataset.theme ||
      (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const next = current === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try {
      localStorage.setItem("theme", next);
    } catch (e) {}
  });
})();
