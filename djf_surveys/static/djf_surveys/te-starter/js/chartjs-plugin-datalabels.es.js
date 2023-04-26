import { m as g, t as T, r as u, d as A, a as E, v as B, c as z, i as P, A as W, P as N, B as O } from "./chart.es.js";
/*!
 * chartjs-plugin-datalabels v2.2.0
 * https://chartjs-plugin-datalabels.netlify.app
 * (c) 2017-2022 chartjs-plugin-datalabels contributors
 * Released under the MIT license
 */
var M = function() {
  if (typeof window < "u") {
    if (window.devicePixelRatio)
      return window.devicePixelRatio;
    var r = window.screen;
    if (r)
      return (r.deviceXDPI || 1) / (r.logicalXDPI || 1);
  }
  return 1;
}(), c = {
  // @todo move this in Chart.helpers.toTextLines
  toTextLines: function(r) {
    var e = [], a;
    for (r = [].concat(r); r.length; )
      a = r.pop(), typeof a == "string" ? e.unshift.apply(e, a.split(`
`)) : Array.isArray(a) ? r.push.apply(r, a) : P(r) || e.unshift("" + a);
    return e;
  },
  // @todo move this in Chart.helpers.canvas.textSize
  // @todo cache calls of measureText if font doesn't change?!
  textSize: function(r, e, a) {
    var t = [].concat(e), i = t.length, n = r.font, o = 0, s;
    for (r.font = a.string, s = 0; s < i; ++s)
      o = Math.max(r.measureText(t[s]).width, o);
    return r.font = n, {
      height: i * a.lineHeight,
      width: o
    };
  },
  /**
   * Returns value bounded by min and max. This is equivalent to max(min, min(value, max)).
   * @todo move this method in Chart.helpers.bound
   * https://doc.qt.io/qt-5/qtglobal.html#qBound
   */
  bound: function(r, e, a) {
    return Math.max(r, Math.min(e, a));
  },
  /**
   * Returns an array of pair [value, state] where state is:
   * * -1: value is only in a0 (removed)
   * *  1: value is only in a1 (added)
   */
  arrayDiff: function(r, e) {
    var a = r.slice(), t = [], i, n, o, s;
    for (i = 0, o = e.length; i < o; ++i)
      s = e[i], n = a.indexOf(s), n === -1 ? t.push([s, 1]) : a.splice(n, 1);
    for (i = 0, o = a.length; i < o; ++i)
      t.push([a[i], -1]);
    return t;
  },
  /**
   * https://github.com/chartjs/chartjs-plugin-datalabels/issues/70
   */
  rasterize: function(r) {
    return Math.round(r * M) / M;
  }
};
function p(r, e) {
  var a = e.x, t = e.y;
  if (a === null)
    return { x: 0, y: -1 };
  if (t === null)
    return { x: 1, y: 0 };
  var i = r.x - a, n = r.y - t, o = Math.sqrt(i * i + n * n);
  return {
    x: o ? i / o : 0,
    y: o ? n / o : -1
  };
}
function D(r, e, a, t, i) {
  switch (i) {
    case "center":
      a = t = 0;
      break;
    case "bottom":
      a = 0, t = 1;
      break;
    case "right":
      a = 1, t = 0;
      break;
    case "left":
      a = -1, t = 0;
      break;
    case "top":
      a = 0, t = -1;
      break;
    case "start":
      a = -a, t = -t;
      break;
    case "end":
      break;
    default:
      i *= Math.PI / 180, a = Math.cos(i), t = Math.sin(i);
      break;
  }
  return {
    x: r,
    y: e,
    vx: a,
    vy: t
  };
}
var F = 0, I = 1, S = 2, R = 4, C = 8;
function _(r, e, a) {
  var t = F;
  return r < a.left ? t |= I : r > a.right && (t |= S), e < a.top ? t |= C : e > a.bottom && (t |= R), t;
}
function G(r, e) {
  for (var a = r.x0, t = r.y0, i = r.x1, n = r.y1, o = _(a, t, e), s = _(i, n, e), v, l, h; !(!(o | s) || o & s); )
    v = o || s, v & C ? (l = a + (i - a) * (e.top - t) / (n - t), h = e.top) : v & R ? (l = a + (i - a) * (e.bottom - t) / (n - t), h = e.bottom) : v & S ? (h = t + (n - t) * (e.right - a) / (i - a), l = e.right) : v & I && (h = t + (n - t) * (e.left - a) / (i - a), l = e.left), v === o ? (a = l, t = h, o = _(a, t, e)) : (i = l, n = h, s = _(i, n, e));
  return {
    x0: a,
    x1: i,
    y0: t,
    y1: n
  };
}
function b(r, e) {
  var a = e.anchor, t = r, i, n;
  return e.clamp && (t = G(t, e.area)), a === "start" ? (i = t.x0, n = t.y0) : a === "end" ? (i = t.x1, n = t.y1) : (i = (t.x0 + t.x1) / 2, n = (t.y0 + t.y1) / 2), D(i, n, r.vx, r.vy, e.align);
}
var m = {
  arc: function(r, e) {
    var a = (r.startAngle + r.endAngle) / 2, t = Math.cos(a), i = Math.sin(a), n = r.innerRadius, o = r.outerRadius;
    return b({
      x0: r.x + t * n,
      y0: r.y + i * n,
      x1: r.x + t * o,
      y1: r.y + i * o,
      vx: t,
      vy: i
    }, e);
  },
  point: function(r, e) {
    var a = p(r, e.origin), t = a.x * r.options.radius, i = a.y * r.options.radius;
    return b({
      x0: r.x - t,
      y0: r.y - i,
      x1: r.x + t,
      y1: r.y + i,
      vx: a.x,
      vy: a.y
    }, e);
  },
  bar: function(r, e) {
    var a = p(r, e.origin), t = r.x, i = r.y, n = 0, o = 0;
    return r.horizontal ? (t = Math.min(r.x, r.base), n = Math.abs(r.base - r.x)) : (i = Math.min(r.y, r.base), o = Math.abs(r.base - r.y)), b({
      x0: t,
      y0: i + o,
      x1: t + n,
      y1: i,
      vx: a.x,
      vy: a.y
    }, e);
  },
  fallback: function(r, e) {
    var a = p(r, e.origin);
    return b({
      x0: r.x,
      y0: r.y,
      x1: r.x + (r.width || 0),
      y1: r.y + (r.height || 0),
      vx: a.x,
      vy: a.y
    }, e);
  }
}, f = c.rasterize;
function L(r) {
  var e = r.borderWidth || 0, a = r.padding, t = r.size.height, i = r.size.width, n = -i / 2, o = -t / 2;
  return {
    frame: {
      x: n - a.left - e,
      y: o - a.top - e,
      w: i + a.width + e * 2,
      h: t + a.height + e * 2
    },
    text: {
      x: n,
      y: o,
      w: i,
      h: t
    }
  };
}
function H(r, e) {
  var a = e.chart.getDatasetMeta(e.datasetIndex).vScale;
  if (!a)
    return null;
  if (a.xCenter !== void 0 && a.yCenter !== void 0)
    return { x: a.xCenter, y: a.yCenter };
  var t = a.getBasePixel();
  return r.horizontal ? { x: t, y: null } : { x: null, y: t };
}
function X(r) {
  return r instanceof W ? m.arc : r instanceof N ? m.point : r instanceof O ? m.bar : m.fallback;
}
function j(r, e, a, t, i, n) {
  var o = Math.PI / 2;
  if (n) {
    var s = Math.min(n, i / 2, t / 2), v = e + s, l = a + s, h = e + t - s, d = a + i - s;
    r.moveTo(e, l), v < h && l < d ? (r.arc(v, l, s, -Math.PI, -o), r.arc(h, l, s, -o, 0), r.arc(h, d, s, 0, o), r.arc(v, d, s, o, Math.PI)) : v < h ? (r.moveTo(v, a), r.arc(h, l, s, -o, o), r.arc(v, l, s, o, Math.PI + o)) : l < d ? (r.arc(v, l, s, -Math.PI, 0), r.arc(v, d, s, 0, Math.PI)) : r.arc(v, l, s, -Math.PI, Math.PI), r.closePath(), r.moveTo(e, a);
  } else
    r.rect(e, a, t, i);
}
function q(r, e, a) {
  var t = a.backgroundColor, i = a.borderColor, n = a.borderWidth;
  !t && (!i || !n) || (r.beginPath(), j(
    r,
    f(e.x) + n / 2,
    f(e.y) + n / 2,
    f(e.w) - n,
    f(e.h) - n,
    a.borderRadius
  ), r.closePath(), t && (r.fillStyle = t, r.fill()), i && n && (r.strokeStyle = i, r.lineWidth = n, r.lineJoin = "miter", r.stroke()));
}
function J(r, e, a) {
  var t = a.lineHeight, i = r.w, n = r.x, o = r.y + t / 2;
  return e === "center" ? n += i / 2 : (e === "end" || e === "right") && (n += i), {
    h: t,
    w: i,
    x: n,
    y: o
  };
}
function U(r, e, a) {
  var t = r.shadowBlur, i = a.stroked, n = f(a.x), o = f(a.y), s = f(a.w);
  i && r.strokeText(e, n, o, s), a.filled && (t && i && (r.shadowBlur = 0), r.fillText(e, n, o, s), t && i && (r.shadowBlur = t));
}
function $(r, e, a, t) {
  var i = t.textAlign, n = t.color, o = !!n, s = t.font, v = e.length, l = t.textStrokeColor, h = t.textStrokeWidth, d = l && h, y;
  if (!(!v || !o && !d))
    for (a = J(a, i, s), r.font = s.string, r.textAlign = i, r.textBaseline = "middle", r.shadowBlur = t.textShadowBlur, r.shadowColor = t.textShadowColor, o && (r.fillStyle = n), d && (r.lineJoin = "round", r.lineWidth = h, r.strokeStyle = l), y = 0, v = e.length; y < v; ++y)
      U(r, e[y], {
        stroked: d,
        filled: o,
        w: a.w,
        x: a.x,
        y: a.y + a.h * y
      });
}
var K = function(r, e, a, t) {
  var i = this;
  i._config = r, i._index = t, i._model = null, i._rects = null, i._ctx = e, i._el = a;
};
g(K.prototype, {
  /**
   * @private
   */
  _modelize: function(r, e, a, t) {
    var i = this, n = i._index, o = T(u([a.font, {}], t, n)), s = u([a.color, A.color], t, n);
    return {
      align: u([a.align, "center"], t, n),
      anchor: u([a.anchor, "center"], t, n),
      area: t.chart.chartArea,
      backgroundColor: u([a.backgroundColor, null], t, n),
      borderColor: u([a.borderColor, null], t, n),
      borderRadius: u([a.borderRadius, 0], t, n),
      borderWidth: u([a.borderWidth, 0], t, n),
      clamp: u([a.clamp, !1], t, n),
      clip: u([a.clip, !1], t, n),
      color: s,
      display: r,
      font: o,
      lines: e,
      offset: u([a.offset, 4], t, n),
      opacity: u([a.opacity, 1], t, n),
      origin: H(i._el, t),
      padding: E(u([a.padding, 4], t, n)),
      positioner: X(i._el),
      rotation: u([a.rotation, 0], t, n) * (Math.PI / 180),
      size: c.textSize(i._ctx, e, o),
      textAlign: u([a.textAlign, "start"], t, n),
      textShadowBlur: u([a.textShadowBlur, 0], t, n),
      textShadowColor: u([a.textShadowColor, s], t, n),
      textStrokeColor: u([a.textStrokeColor, s], t, n),
      textStrokeWidth: u([a.textStrokeWidth, 0], t, n)
    };
  },
  update: function(r) {
    var e = this, a = null, t = null, i = e._index, n = e._config, o, s, v, l = u([n.display, !0], r, i);
    l && (o = r.dataset.data[i], s = B(z(n.formatter, [o, r]), o), v = P(s) ? [] : c.toTextLines(s), v.length && (a = e._modelize(l, v, n, r), t = L(a))), e._model = a, e._rects = t;
  },
  geometry: function() {
    return this._rects ? this._rects.frame : {};
  },
  rotation: function() {
    return this._model ? this._model.rotation : 0;
  },
  visible: function() {
    return this._model && this._model.opacity;
  },
  model: function() {
    return this._model;
  },
  draw: function(r, e) {
    var a = this, t = r.ctx, i = a._model, n = a._rects, o;
    this.visible() && (t.save(), i.clip && (o = i.area, t.beginPath(), t.rect(
      o.left,
      o.top,
      o.right - o.left,
      o.bottom - o.top
    ), t.clip()), t.globalAlpha = c.bound(0, i.opacity, 1), t.translate(f(e.x), f(e.y)), t.rotate(i.rotation), q(t, n.frame, i), $(t, i.lines, n.text, i), t.restore());
  }
});
var Q = Number.MIN_SAFE_INTEGER || -9007199254740991, V = Number.MAX_SAFE_INTEGER || 9007199254740991;
function x(r, e, a) {
  var t = Math.cos(a), i = Math.sin(a), n = e.x, o = e.y;
  return {
    x: n + t * (r.x - n) - i * (r.y - o),
    y: o + i * (r.x - n) + t * (r.y - o)
  };
}
function k(r, e) {
  var a = V, t = Q, i = e.origin, n, o, s, v, l;
  for (n = 0; n < r.length; ++n)
    o = r[n], s = o.x - i.x, v = o.y - i.y, l = e.vx * s + e.vy * v, a = Math.min(a, l), t = Math.max(t, l);
  return {
    min: a,
    max: t
  };
}
function w(r, e) {
  var a = e.x - r.x, t = e.y - r.y, i = Math.sqrt(a * a + t * t);
  return {
    vx: (e.x - r.x) / i,
    vy: (e.y - r.y) / i,
    origin: r,
    ln: i
  };
}
var Y = function() {
  this._rotation = 0, this._rect = {
    x: 0,
    y: 0,
    w: 0,
    h: 0
  };
};
g(Y.prototype, {
  center: function() {
    var r = this._rect;
    return {
      x: r.x + r.w / 2,
      y: r.y + r.h / 2
    };
  },
  update: function(r, e, a) {
    this._rotation = a, this._rect = {
      x: e.x + r.x,
      y: e.y + r.y,
      w: e.w,
      h: e.h
    };
  },
  contains: function(r) {
    var e = this, a = 1, t = e._rect;
    return r = x(r, e.center(), -e._rotation), !(r.x < t.x - a || r.y < t.y - a || r.x > t.x + t.w + a * 2 || r.y > t.y + t.h + a * 2);
  },
  // Separating Axis Theorem
  // https://gamedevelopment.tutsplus.com/tutorials/collision-detection-using-the-separating-axis-theorem--gamedev-169
  intersects: function(r) {
    var e = this._points(), a = r._points(), t = [
      w(e[0], e[1]),
      w(e[0], e[3])
    ], i, n, o;
    for (this._rotation !== r._rotation && t.push(
      w(a[0], a[1]),
      w(a[0], a[3])
    ), i = 0; i < t.length; ++i)
      if (n = k(e, t[i]), o = k(a, t[i]), n.max < o.min || o.max < n.min)
        return !1;
    return !0;
  },
  /**
   * @private
   */
  _points: function() {
    var r = this, e = r._rect, a = r._rotation, t = r.center();
    return [
      x({ x: e.x, y: e.y }, t, a),
      x({ x: e.x + e.w, y: e.y }, t, a),
      x({ x: e.x + e.w, y: e.y + e.h }, t, a),
      x({ x: e.x, y: e.y + e.h }, t, a)
    ];
  }
});
//# sourceMappingURL=chartjs-plugin-datalabels.es.js.map
