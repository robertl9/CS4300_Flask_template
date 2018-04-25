$(document).ready(function() {

  $(".bootstrap-tagsinput").on("keypress", function(e) {
    if (e.keyCode == 13){
      e.preventDefault();
      e.keyCode = 188;
    };
  });

  $("#include").lc_switch("INCLUDE", "EXCLUDE");

  $(".dish-panel>.panel-heading").on("click", function() {
    $(this).parent().find(".panel-body").toggle(300);
  });

  $("img").on("error", function() {
    $(this).attr('src', '/static/assets/defimage.png');
  });

});

function autocomplete(inp, otp, arr, tags) {

  let queries = [];

  let ingrs = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: $.grep(arr, function(item) { return item.length <= 10 })
  });
  ingrs.initialize();

  inp.tagsinput({
    tagClass: function() {
      if ($("#include").prop("checked")) {
        return "label label-success";
      } else {
        return "label label-danger label-important";
      }
    },
    typeaheadjs: {
      source: ingrs.ttAdapter()
    },
    freeInput: false
  });
  inp.on('itemAdded', function(event) {
    queries.push({"item": event.item, "include": $("#include").prop("checked")});
  });
  inp.on('itemRemoved', function(event) {
    queries = $.grep(queries, function(query) { return query.item !== event.item; });
  });

  for (let i = 0; i < tags.length; i++) {
    $("#include").prop("checked", tags[i][1]);
    inp.tagsinput('add', tags[i][0]);
  }

  $('#inputs').submit(function() {
    let input = "";
    queries.forEach(function(query) {
      input += query.item + '|' + (query.include ? 1 : 0) + ','
    })
    otp.val(input);
    return true;
});

}

function displayRating(div, rating) {
  rating = Math.round(rating / 2) / 10;
  for (var i = 0; i < 5; i++) {
    let star = $("<i class='fa fa-2x'></i>");
    if (rating < i + 0.3) {
      star.addClass("fa-star-o");
    } else if (rating < i + 0.8) {
      star.addClass("fa-star-half-o");
    } else {
      star.addClass("fa-star");
    }
    div.append(star);
  }
  div.append("<div>" + rating.toFixed(1) + "</div>");
}