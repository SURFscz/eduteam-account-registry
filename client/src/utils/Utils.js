export function stopEvent(e) {
  if (e !== undefined && e !== null) {
    e.preventDefault();
    e.stopPropagation();
  }
}

export function isEmpty(obj) {
  if (obj === undefined || obj === null) {
    return true;
  }
  if (Array.isArray(obj)) {
    return obj.length === 0;
  }
  if (typeof obj === "string") {
    return obj.trim().length === 0;
  }
  if (typeof obj === "object") {
    return Object.keys(obj).length === 0;
  }
  return false;
}

export function groupBy(arr, key) {
  return arr.reduce((acc, item) => {
    (acc[item[key]] = acc[item[key]] || []).push(item);
    return acc;
  }, {});
}

const S4 = () => (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);

export function pseudoGuid() {
  return (S4() + S4() + "-" + S4() + "-4" + S4().substr(0, 3) + "-" + S4() + "-" + S4() + S4() + S4()).toLowerCase();
}

