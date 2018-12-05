$(document).ready(function(){
    $('form').on('submit',function(event){
      document.querySelector('.div1').classList.add('progress')
      document.querySelector('.div2').classList.add('indeterminate')
      setTimeout(function(){
        document.querySelector('.div1').classList.remove('progress')
        document.querySelector('.div2').classList.remove('indeterminate')
      },7550);
      $.ajax({
        data:{
          wineName:$('#wineName').val(),
          price:$('#price').val()
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
            // let myUL=$('<ul class="collection"></ul>')
            // let myLI=$('<li class="collection-item avatar"><img src='+value.url+' alt="wine Image" class="circle" style="max-height: 100px"><h4 class="title">'+value.name+'</h4><p><i class="material-icons">location_on</i>'+value.region+'<p><i class="material-icons">attach_money</i>'+value.price+'</i></p><a href="#!" class="secondary-content"><i class="material-icons addBtn" wineid='+value.id+' >add</i></a>')
            // myLI.appendTo(myUL)
            // myUL.appendTo('#content');

            // let mainDiv=$('<div class="col s6 m3"></div>')
            // let O=$('<div class="card horizontal"><div class="card-image"><img src='+value.url+' style="max-height: 500px; padding: 10px></div><div class="card-stacked"><div class="card-content"><p>'+value.name+'</p></div><div class="card-action"><a href="#">This is a link</a></div></div></div></div>')
            // O.appendTo(mainDiv)
            // mainDiv.appendTo('#result')

          let mainDiv=$('<div class="col s6 m3"></div>')
          let O=$('<div style="height: 400px" class="card" style="height: 400px"><div class="card-image waves-effect waves-block waves-light"><img src='+value.url+' style="max-height: 400px; padding: 10px"></div><div class="card-content"><span class="card-title">'+value.name+ '</span></div><a class="btn-floating halfway-fab waves-effect waves-light red addBtn" wineid='+value.id+'><i class="material-icons">add</i></a> <p><i class="material-icons">location_on</i>' +value.region+'</p>')
          O.appendTo(mainDiv)
          mainDiv.appendTo('#result')
        });
        }
      })
      event.preventDefault()

    });
});
