document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.autocomplete');
    var instances = M.Autocomplete.init(elems, options);
  });

$(document).ready(function(){
  // $('').click(function(){
  //   $.ajax("{{url_for('dashboared')}}".done(function(reply){
  //     $('#searchContent').html(reply)
  //   })


  // });
//   $('#searchBtn').click(function(){
//     var word = $('#searchBtn').val();
//     $.ajax({
//     url: "/dash",
//     type: "get",
//     data: {word: word},
//     success: function(response) {
//     $("#searchContent").html(searchCards.html);
//    },
//    error: function(xhr) {
//      //Do Something to handle error
//   }
//   });
// });

  $.get('searchCards.html',function(data){
    console.log(data);
      $('#searchContent').html(data);
  });


  $('.addBtn').on('click',function(){
    let wineID=$(this).attr('wineID');

    req=$.ajax({
      url:'/save',
      type:'POST',
      data:{ id:wineID }
    })
  })
});
