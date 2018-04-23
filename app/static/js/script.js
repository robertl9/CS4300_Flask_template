$(document).ready(function() {

  $(".bootstrap-tagsinput").on("keypress", function(e) {
    if (e.keyCode == 13){
      e.preventDefault();
      e.keyCode = 188;
    };
  });

  $(".dish-panel>.panel-heading").on("click", function() {
    $(this).parent().find(".panel-body").toggle(300);
  });

  $("#include").lc_switch("INCLUDE", "EXCLUDE");

});

function autocomplete(inp, otp, arr, tags) {

  var queries = [];

  var ingrs = new Bloodhound({
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

  for (var i = 0; i < tags.length; i++) {
    $("#include").prop("checked", tags[i][1]);
    inp.tagsinput('add', tags[i][0]);
  }

  $('#inputs').submit(function() {
    var input = "";
    queries.forEach(function(query) {
      input += query.item + '|' + (query.include ? 1 : 0) + ','
    })
    otp.val(input);
    return true;
});

}