const $cru = (e) => document.querySelector(e),
  $crus = (e) => document.querySelectorAll(e),
  $cruConfig = {
    prefix_url: "",
    headers: { "Content-Type": "application/json" },
    callbacks: {},
  },
  $C = (e = false) => {
    if (e) for (let t of Object.keys(e)) $cruConfig[t] = e[t];
    $cruLoadEvents();
  },
  $cruLoadEvents = () => {
    $cruLoadRequests();
    $cruLoadFormIntercept();
    $cruLoadAllContainers();
  },
  $cruLoadContainer = async (el) => {
    el.classList.add("loaded");
    const container = el.closest("[c-container]") || el,
      url = container.getAttribute("c-container"),
      targetSelector = container.getAttribute("c-target") || false,
      type = container.getAttribute("c-type") || "html",
      callbackName = container.getAttribute("c-callback") || false,
      res = await fetch($cruConfig.prefix_url + url, {
        method: "GET",
        headers: $cruConfig.headers,
      }),
      content = await $cruTypeResponse(type, res),
      target = targetSelector ? $cru(targetSelector) : container;

    if (targetSelector || targetSelector !== "off") {
      targetSelector
        ? (target.innerHTML = content)
        : type === "html" && (target.innerHTML = content);
    }

    if (callbackName && $cruConfig.callbacks[callbackName]) {
      $cruConfig.callbacks[callbackName]();
    }

    $cruLoadEvents();
  },
  $cruLoadAllContainers = async () => {
    for (const el of $crus("[c-container]:not(.loaded)")) {
      el.classList.add("loaded");
      await $cruLoadContainer(el);
    }

    for (const el of $crus("[c-reload]:not(.loaded)")) {
      el.classList.add("loaded");
      el.addEventListener("click", () => $cruLoadContainer(el));
    }
  },
  cruRequest = async (el, method) => {
    const url = el.getAttribute(`c-${method}`),
      type = el.getAttribute("c-type") || "html",
      reloadContainer = el.getAttribute("c-reload-container") || false,
      removeClosest = el.getAttribute("c-remove-closest") || false,
      selfRemove = el.getAttribute("c-self-remove") || false,
      redirect = el.getAttribute("c-redirect") || false,
      swap = el.getAttribute("c-swap") || false,
      append = el.getAttribute("c-append") || false,
      prepend = el.getAttribute("c-prepend") || false,
      callbackName = el.getAttribute("c-callback") || false,
      targetSelector = el.getAttribute("c-target") || false,
      res = await fetch($cruConfig.prefix_url + url, {
        method,
        headers: $cruConfig.headers,
      }),
      content = await $cruTypeResponse(type, res),
      target = !!targetSelector && $cru(targetSelector);

    if (removeClosest) el.closest(removeClosest)?.remove();
    if (selfRemove) el.remove();
    if (swap) $cru(swap).outerHTML = content;
    if (append) $cru(append).insertAdjacentHTML("beforeend", content);
    if (prepend) $cru(prepend).insertAdjacentHTML("afterbegin", content);
    if (reloadContainer) $cruLoadContainer(el);
    if (target) {
      target.innerHTML = content;
    } else if (type === "html") {
      el.innerHTML = content;
    }

    if (callbackName && $cruConfig.callbacks[callbackName]) {
      $cruConfig.callbacks[callbackName]();
    }

    $cruLoadEvents();

    if (redirect) window.location.href = redirect;
  },
  $cruLoadRequests = () => {
    $crus("[c-delete]:not(.loaded)").forEach((el) => {
      el.classList.add("loaded");
      el.addEventListener("click", () => {
        cruRequest(el, "delete");
      });
    });

    $crus("[c-put]:not(.loaded)").forEach((el) => {
      el.classList.add("loaded");
      el.addEventListener("click", () => {
        cruRequest(el, "put");
      });
    });

    $crus("[c-get]:not(.loaded)").forEach((el) => {
      el.classList.add("loaded");
      el.addEventListener("click", () => {
        cruRequest(el, "get");
      });
    });

    $crus("[c-post]:not(.loaded)").forEach((el) => {
      el.classList.add("loaded");
      el.addEventListener("click", () => {
        cruRequest(el, "post");
      });
    });
  },
  $cruLoadFormIntercept = () => {
    $crus(".c-form:not(.loaded)").forEach((form) => {
      form.classList.add("loaded");

      form.addEventListener("submit", async (t) => {
        t.preventDefault();

        const action = form.getAttribute("action");
        const method = form.getAttribute("method").toUpperCase() || "POST";
        const type = form.getAttribute("c-type") || "html";
        const append = form.getAttribute("c-append") || false;
        const prepend = form.getAttribute("c-prepend") || false;
        const redirect = form.getAttribute("c-redirect") || false;
        const reset = form.getAttribute("c-reset") || false;
        const swap = form.getAttribute("c-swap") || false;
        const targetSelector = form.getAttribute("c-target") || false;
        const reloadContainer =
          form.getAttribute("c-reload-container") || false;
        const callbackName = form.getAttribute("c-callback") || false;

        const isReadMethod = $cruIsRead(method);
        const formData = Object.fromEntries(new FormData(form).entries());
        const url = cruFormatURL(action, isReadMethod, formData);

        const res = await fetch(url, {
          method,
          headers: $cruConfig.headers,
          body: isReadMethod ? null : JSON.stringify(formData),
        });

        if (!res.ok) {
          // Se a resposta for um erro, trate aqui
          let responseError = await res.json();
          console.error("Erro ao enviar produto:", responseError.error);

          // Aqui você pode exibir uma mensagem de erro na interface
          // Exemplo: Exibir um alerta com a mensagem de erro
          const errorDiv = document.createElement("div");
          errorDiv.className = "alert alert-danger mt-2";
          errorDiv.textContent = responseError.error || "Erro desconhecido.";
          form.prepend(errorDiv);
          return;
        }

        let response;
        try {
          response = await res.json(); // Tente converter a resposta para JSON
        } catch (err) {
          console.error("Erro ao interpretar a resposta:", err);
          return;
        }

        // Caso de sucesso, trate a resposta aqui
        if (res.ok) {
          const successDiv = document.createElement("div");
          successDiv.className = "alert alert-success mt-2";
          successDiv.textContent =
            response.message || "Produto inserido com sucesso.";
          form.prepend(successDiv);
        }

        // ✅ Sucesso: mostra mensagem se houver
        if (res.ok && type === "json" && response.message) {
          const successDiv = document.createElement("div");
          successDiv.className = "alert alert-success mt-2";
          successDiv.textContent = response.message;
          form.prepend(successDiv);
        }

        // Manipulação de destino
        if (typeof response === "string") {
          if (swap) $cru(swap).outerHTML = response;
          if (append) $cru(append).insertAdjacentHTML("beforeend", response);
          if (prepend) $cru(prepend).insertAdjacentHTML("afterbegin", response);
          if (targetSelector) $cru(targetSelector).innerHTML = response;
        }

        // Limpa o formulário se a resposta for OK
        if (reset && res.ok) form.reset();

        // Recarrega container se configurado
        if (reloadContainer) $cruLoadContainer(form);

        // Executa callback, se existir
        if (callbackName && $cruConfig.callbacks[callbackName]) {
          $cruConfig.callbacks[callbackName]({ status: res.status, response });
        }

        // Redireciona se houver
        if (redirect) window.location.href = redirect;
      });
    });
  };

(cruFormatURL = (url, isRead, data) => {
  let fullURL = $cruConfig.prefix_url + url;
  if (isRead) {
    try {
      fullURL = new URL(url);
    } catch (e) {
      try {
        fullURL = new URL(window.location.origin + url);
      } catch (err) {
        throw url;
      }
    } finally {
      fullURL.search = new URLSearchParams(data).toString();
      fullURL = fullURL.href;
    }
  }
  return fullURL;
}),
  ($cruCallback = (name, fn) => {
    $cruConfig.callbacks[name] = fn;
  }),
  ($cruIsRead = (method) => ["GET", "HEAD"].includes(method)),
  ($cruTypeResponse = async (type, res) =>
    type === "html" ? await res.text() : await res.json());

$C();

// Exemplo de callback
$cruCallback("updateTitle", () => {
  const button = document.activeElement;
  const newTitle = button.getAttribute("data-title");
  const titleElement = document.getElementById("page-title");

  if (newTitle && titleElement) {
    titleElement.textContent = newTitle;
  }
});
