clearTimeout(window._filter_render_data_timeout);

function updateSource(source, origin, date_range) {
  const x = origin.data["index"];

  // console.log(x)

  let start = 0;
  for (let i = 0; i < x.length; i++) {
    if (x[i] >= date_range[0]) {
      start = i;
      break;
    }
  }

  let end = x.length;
  for (let i = start; i < x.length; i++) {
    if (x[i] >= date_range[1]) {
      end = i + 1;
      break;
    }
  }

  for (let column of Object.keys(source.data)) {
    source.data[column] = origin.data[column].slice(start, end);
  }

  source.change.emit();
}

// console.log("update render range file");

window._filter_render_data_timeout = setTimeout(function () {
  let date_range = cb_obj.value;

  // set minimum date range
  const day = 1000 * 60 * 60 * 24;

  if (date_range[1] - date_range[0] < day) {
    date_range[1] = date_range[0] + day;
    date_range[0] -= day;
  }

  // console.log(sources_and_origins);
  // console.log("date_range", date_range);

  for (let so of sources_and_origins) {
    const source = so[0];
    const origin_source = so[1];

    // console.log("source", source);
    // console.log("origin", origin_source);
    // console.log("date_range", date_range);
    updateSource(source, origin_source, date_range);
  }

  x_range.start = date_range[0];
  x_range.end = date_range[1];
}, 50);
