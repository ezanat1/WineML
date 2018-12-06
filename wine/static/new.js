$(document).ready(function(){
    $('form').on('submit',function(event){
      document.querySelector('.div1').classList.add('progress')
      document.querySelector('.div2').classList.add('indeterminate')
      setTimeout(function(){
        document.querySelector('.div1').classList.remove('progress')
        document.querySelector('.div2').classList.remove('indeterminate')
      },7600);
      $.ajax({
        data:{
          wineName:$('#wineName').val(),
          price:$('#price').val(),
          food:$('#food').val()
        },
        type:'POST',
        url:'/process'
      })
      .done(function(data){
        if(data.error){
          console.log('not name')
        }
        else{
          $.each(data, function(key, value) {
          let mainDiv=$('<div class="col s3 m4"></div>')
          let O=$('<div class="card "><div class="card-image waves-effect waves-block waves-light"><img src='+value.url+' style="max-height: 400px; padding: 10px"><a class="btn-floating right btn-small  waves-effect waves-light red addBtn" wineid='+value.id+'><i class="material-icons">add</i></a></div><div class="card-content"><span style="font-size:20px;font-family:cursive;overflow: hidden">'+value.name+ '</span><p><i class="material-icons">location_on</i>'+value.region+'</p><p><i class="material-icons">attach_money</i>'+value.price+'</p><p><i class="material-icons">restaurant_menu</i>'+value.pairing+'</p></div></div></div>')
          O.appendTo(mainDiv)
          mainDiv.appendTo('#result')
        });
        }
      })
      event.preventDefault()

    });
});
