import spinner from "../utils/Spin";

//Internal API
function validateResponse(showErrorDialog) {
  return res => {
    spinner.stop();

    if (!res.ok) {
      if (res.type === "opaqueredirect") {
        setTimeout(() => window.location.reload(), 100);
        return res;
      }
      const error = new Error(res.statusText);
      error.response = res;

      if (showErrorDialog) {
        setTimeout(() => {
          throw error;
        }, 250);
      }
      throw error;
    }
    const sessionAlive = res.headers.get("x-session-alive");

    if (sessionAlive !== "true") {
      window.location.reload();
    }
    return res;

  };
}

function validFetch(path, options, headers = {}, showErrorDialog = true) {
  const contentHeaders = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    ...headers
  };
  const fetchOptions = Object.assign({}, {headers: contentHeaders}, options, {
    credentials: "same-origin",
    redirect: "manual"
  });
  spinner.start();
  return fetch(path, fetchOptions)
    .then(validateResponse(showErrorDialog))
    .catch(err => {
      spinner.stop();
      throw err;
    });
}

function fetchJson(path, options = {}, headers = {}, showErrorDialog = true) {
  return validFetch(path, options, headers, showErrorDialog)
    .then(res => res.json());
}

function postPutJson(path, body, method, showErrorDialog = true) {
  return fetchJson(path, {method: method, body: JSON.stringify(body)}, {}, showErrorDialog);
}

export function config() {
  return fetchJson("/config");
}

//Users
export function me() {
  return fetchJson("/api/users/me", {}, {}, false);
}

export function updateUser(attributes) {
  return postPutJson("/api/users", attributes, "put");
}

export function completeRegistration() {
  return postPutJson("/api/users/complete", {}, "put");
}

export function reportError(error) {
  return postPutJson("/api/users/error", error, "post");
}

export function verifyEmail(code, email) {
  return postPutJson("/api/users/verify", {"code": code, "email": email}, "post", false);
}

export function regenerateEmail(email) {
  return postPutJson("/api/users/regenerate", {"email": email}, "post", false);
}

export function openEmailVerifications() {
  return fetchJson("/api/users/verifications");
}

export function redirectKey() {
  return fetchJson("/api/users/redirect_key");
}

//Aup
export function aupLinks() {
  return fetchJson("/api/aup");
}

export function agreeAup() {
  return postPutJson("/api/aup", {}, "post");
}

