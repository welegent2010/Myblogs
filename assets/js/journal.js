/* 王晓东 · 独立研究档案
   原生 JS，无第三方依赖：外观切换 / 阅读进度 / 目录高亮 / 归档筛选 / 站内搜索 */
(function () {
  "use strict";

  /* ---------- 外观切换 ---------- */
  var root = document.documentElement;
  var toggle = document.querySelector("[data-theme-toggle]");

  function paint(theme) {
    root.setAttribute("data-theme", theme);
    try {
      localStorage.setItem("xd-theme", theme);
    } catch (e) {}
    if (toggle) {
      toggle.textContent = theme === "dark" ? "浅色" : "深色";
      toggle.setAttribute("aria-label", theme === "dark" ? "切换到浅色" : "切换到深色");
    }
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      paint(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });
  }
  paint(root.getAttribute("data-theme") || "light");

  /* ---------- 阅读进度 ---------- */
  var bar = document.querySelector(".progress");
  var article = document.querySelector(".prose");
  if (bar && article) {
    var ticking = false;
    var update = function () {
      var rect = article.getBoundingClientRect();
      var total = rect.height - window.innerHeight;
      var passed = -rect.top;
      var pct = total > 0 ? Math.min(100, Math.max(0, (passed / total) * 100)) : 0;
      bar.style.width = pct.toFixed(2) + "%";
      ticking = false;
    };
    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          ticking = true;
          window.requestAnimationFrame(update);
        }
      },
      { passive: true }
    );
    window.addEventListener("resize", update, { passive: true });
    update();
  }

  /* ---------- 目录高亮 ---------- */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc--sticky a[href^='#']"));
  if (tocLinks.length) {
    var headings = tocLinks
      .map(function (a) {
        return document.getElementById(decodeURIComponent(a.getAttribute("href").slice(1)));
      })
      .filter(Boolean);

    var syncToc = function () {
      var current = null;
      for (var i = 0; i < headings.length; i++) {
        if (headings[i].getBoundingClientRect().top - 120 <= 0) {
          current = headings[i];
        } else {
          break;
        }
      }
      tocLinks.forEach(function (a) {
        a.classList.remove("is-active");
      });
      if (current) {
        var active = document.querySelector(".toc--sticky a[href='#" + current.id + "']");
        if (active) active.classList.add("is-active");
      }
    };
    window.addEventListener("scroll", syncToc, { passive: true });
    syncToc();
  }

  /* ---------- 归档筛选 ---------- */
  var filterBar = document.querySelector(".archive-filter");
  if (filterBar) {
    filterBar.addEventListener("click", function (event) {
      var btn = event.target.closest("button");
      if (!btn) return;
      var channel = btn.getAttribute("data-channel");
      Array.prototype.forEach.call(filterBar.querySelectorAll("button"), function (b) {
        b.classList.toggle("is-active", b === btn);
      });
      Array.prototype.forEach.call(document.querySelectorAll(".archive-row"), function (row) {
        row.classList.toggle("is-hidden", channel !== "all" && row.getAttribute("data-channel") !== channel);
      });
      Array.prototype.forEach.call(document.querySelectorAll(".archive-year"), function (year) {
        var visible = year.querySelectorAll(".archive-row:not(.is-hidden)").length;
        year.classList.toggle("is-hidden", visible === 0);
      });
    });
  }

  /* ---------- 站内搜索 ---------- */
  var input = document.querySelector("#search-query");
  var results = document.querySelector("#search-results");
  if (input && results) {
    var index = null;
    var pending = null;

    var norm = function (s) {
      return (s || "").toLowerCase();
    };

    var render = function (list, query) {
      if (!query) {
        results.innerHTML = "";
        return;
      }
      if (!list.length) {
        results.innerHTML = '<li><p class="entry__summary">没有匹配 “' + query.replace(/[<>&]/g, "") + '” 的研究记录。</p></li>';
        return;
      }
      var html = "";
      for (var i = 0; i < Math.min(list.length, 30); i++) {
        var it = list[i];
        html +=
          '<li><div class="entry__meta"><span class="entry__channel">' +
          (it.channel || "") +
          '</span><span class="dot">/</span><span>' +
          (it.date || "") +
          "</span></div>" +
          '<h3 class="entry__title"><a href="' +
          it.permalink +
          '">' +
          it.title +
          "</a></h3>" +
          '<p class="entry__summary">' +
          (it.summary || "") +
          "</p></li>";
      }
      results.innerHTML = html;
    };

    var search = function (query) {
      var q = norm(query).trim();
      if (!index) return;
      if (!q) {
        render([], "");
        return;
      }
      var terms = q.split(/\s+/);
      var scored = [];
      for (var i = 0; i < index.length; i++) {
        var item = index[i];
        var haystack = norm(item.title + " " + item.summary + " " + (item.tags || []).join(" ") + " " + item.channel);
        var score = 0;
        var ok = true;
        for (var j = 0; j < terms.length; j++) {
          if (haystack.indexOf(terms[j]) === -1) {
            ok = false;
            break;
          }
          if (norm(item.title).indexOf(terms[j]) !== -1) score += 3;
          else score += 1;
        }
        if (ok) scored.push({ item: item, score: score });
      }
      scored.sort(function (a, b) {
        return b.score - a.score || (a.item.date < b.item.date ? 1 : -1);
      });
      render(
        scored.map(function (s) {
          return s.item;
        }),
        query
      );
    };

    fetch("/index.json")
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        index = (data && data.items) || data || [];
        if (pending) {
          search(pending);
          pending = null;
        }
      })
      .catch(function () {
        results.innerHTML = '<li><p class="entry__summary">搜索索引加载失败。</p></li>';
      });

    input.addEventListener("input", function () {
      if (index) search(input.value);
      else pending = input.value;
    });
  }
})();
