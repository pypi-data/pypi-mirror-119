const timeout_name = '_autoscale_timeout_' + unique_name;

clearTimeout(window[timeout_name]);

window[timeout_name] = setTimeout(function () {
  let index = source.data.index;
  let start = cb_obj.start;
  let end = cb_obj.end;
  let min = 1e100;
  let max = -1e10;

  for (let column of columns) {
    for (var i = 0; i < index.length; ++i) {
      if (
        !isNaN(source.data[column][i]) &&
        start <= index[i] &&
        index[i] <= end
      ) {
        max = Math.max(source.data[column][i], max);
        min = Math.min(source.data[column][i], min);
      }
    }
  }

  // console.log("min, max: ", min, max);
  // console.log("start, end: ", start, end);
  // console.log("source.data ", source.data);

  var pad = (max - min) * 0.05;

  y_range.start = min - pad;
  y_range.end = max + pad;
}, 200);
