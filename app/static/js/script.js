$(document).ready(function() {

  $(".bootstrap-tagsinput").on("keypress", function(e) {
    if (e.keyCode == 13){
      e.preventDefault();
      e.keyCode = 188;
    };
  });
  $("#include").lc_switch("INCLUDE", "EXCLUDE");

  sliderTooltip();

});

function sliderTooltip() {

  let tooltip = $("<div class='slider-tooltip' />").hide();
  let setPos = function(val) {
    tooltip.css("top", 15 * (10-val) - 8 + "px");
    tooltip.text(val);
  }

  $("#slider-group>div").hover(function() {
    $(this).append(tooltip);
    setPos($(this).find(".slider").val());
    tooltip.show();
  }, function() {
    tooltip.hide();
  });
  $(".slider").on("input", function() {
    setPos($(this).val());
  });

}

function autocomplete(inp, otp, arr, tags) {

  let queries = [];

  let ingrs = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: $.grep(arr, function(item) {
      return item.indexOf(' ') < 0 && !item.endsWith('s');
    })
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

function multiselect(inp, arr) {

  inp.multiselect({
    dropUp: true,
    maxHeight: 200,
    numberDisplayed: 4,
    buttonWidth: "440px",
    buttonClass: "btn btn-default",
    nonSelectedText: "Select restrictions (optional)"
  });

  inp.multiselect("select", arr);

}

function showResults(temp, data, step) {

  let n = 0;

  let showNext = function() {
      for (let i = n; i < n+step; i++) {
        let d = data[i];
        if (!d) break;
        makePanel(temp, d);
      }
      n += step;
      if (n >= data.length) {
        $("#alert-show").hide();
        $("#alert-end").show().appendTo("#outputs");
      } else {
        $("#alert-end").hide();
        $("#alert-show").show().appendTo("#outputs");
      }
  }

  showNext();

  $("#alert-show").on("click", showNext);

}

function makePanel(temp, d) {
  let panel = temp.clone().attr("id", "dish" + i);
  panel.find(".panel-heading").css("background-image", "url("+d["image"]+")");
  panel.find(".dish-title").text(d["title"]);
  panel.find(".dish-image").attr("src", d["image"]);
  if (d["rating"] && d["rating"] > 0) {
    displayRating(panel.find(".dish-rating"), d["rating"]);
  } else {
    displayRating(panel.find(".dish-rating"), d["spoonacularScore"]);
  }
  panel.find(".dish-note>a").attr("href", d["sourceUrl"]);
  for (var i = 0; i < d["extendedIngredients"].length; i++) {
    panel.find(".dish-ingrs").append(
      '<li class="list-group-item">' +
        d["extendedIngredients"][i]["originalString"] + 
      '</li>');
  }
  panel.find(".dish-descs").text(d["instructions"]);
  panel.show();
  $("#outputs").append(panel);

  panel.find(".panel-heading").on("click", function() {
    panel.find(".panel-body").toggle(300);
  });

  panel.find("img").on("error", function() {
    $(this).attr('src', '/static/assets/defimage.png');
  });
}

function displayRating(div, rating) {
  rating = rating / 2 + 50;
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