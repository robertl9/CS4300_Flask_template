$(document).ready(function() {

  $(".bootstrap-tagsinput").on("keypress", function(e) {
    if (e.keyCode == 13){
      e.preventDefault();
      e.keyCode = 188;
    };
  });

  $(".dish-panel").on("click", function() {
    $(this).find(".panel-body").toggle(300);
  });

});

function autocomplete(inp, otp, arr) {

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

  $('#inputs').submit(function() {
    var input = "";
    queries.forEach(function(query) {
      input += query.item + '|' + (query.include ? 1 : 0) + ','
    })
    otp.val(input);
    return true;
});

}