(function () {
  "use strict";

  // Formulário de contato: monta a mensagem e abre o WhatsApp.
  var form = document.getElementById("wa-form");
  if (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (!form.reportValidity()) return;
      var f = form.elements;
      var d = form.dataset;
      var name = f["name"].value.trim();
      var company = f["company"].value.trim();
      var interest = f["interest"].value;
      var message = f["message"].value.trim();
      var companyPart = company ? d.tplCompany.replace("{company}", company) : "";
      var text = d.tpl
        .replace("{name}", name)
        .replace("{company}", companyPart)
        .replace("{interest}", interest);
      if (message) text += "\n\n" + message;
      var url = "https://wa.me/" + d.number + "?text=" + encodeURIComponent(text);
      window.open(url, "_blank", "noopener");
    });
  }

  // Troca de idioma: leva junto a seção (ou o equipamento) que está na tela.
  // As três versões usam os mesmos ids, então #equipment, #a01 etc. existem em todas.
  function currentAnchor() {
    if (window.scrollY < 120) return "";
    var line = window.innerHeight * 0.33;
    var found = "";
    var els = document.querySelectorAll("main section[id], main article[id]");
    for (var i = 0; i < els.length; i++) {
      if (els[i].getBoundingClientRect().top <= line) found = els[i].id;
    }
    return found ? "#" + found : "";
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest("a.lang-link");
    if (!a || a.getAttribute("aria-current")) return;
    var hash = currentAnchor();
    if (!hash) return;
    ev.preventDefault();
    window.location.href = a.getAttribute("href").split("#")[0] + hash;
  });

  // Menus suspensos do topo (idioma e menu do celular):
  // abre um de cada vez, fecha ao clicar fora, ao escolher um link ou com Esc.
  var menus = document.querySelectorAll(".site-header details");
  function closeAll(except) {
    menus.forEach(function (d) { if (d !== except) d.open = false; });
  }
  menus.forEach(function (d) {
    d.addEventListener("toggle", function () { if (d.open) closeAll(d); });
    d.addEventListener("click", function (ev) {
      if (ev.target.closest("a")) d.open = false;
    });
  });
  document.addEventListener("click", function (ev) {
    menus.forEach(function (d) { if (d.open && !d.contains(ev.target)) d.open = false; });
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key !== "Escape") return;
    menus.forEach(function (d) {
      if (d.open) { d.open = false; d.querySelector("summary").focus(); }
    });
  });
})();
