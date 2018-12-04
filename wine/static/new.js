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
          wineName:$('#wineName').val()
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
            let myUL=$('<ul class="collection"></ul>')
            let myLI=$('<li class="collection-item avatar"><img src='+value.url+' alt="wine Image" class="circle" style="max-height: 100px"><h4 class="title">'+value.name+'</h4><p><i class="material-icons">location_on</i>'+value.region+'<p><i class="material-icons">attach_money</i>'+value.price+'</i></p><a href="#!" class="secondary-content"><i class="material-icons addBtn" >add</i></a>')
            myLI.appendTo(myUL)
            myUL.appendTo('#content');
  });
        }
      })
      event.preventDefault()

    });

    $('.addBtn').on('click',function(){
    let wineID=$(this).attr('wineID');
    console.log(wineID);

    req=$.ajax({
      url:'/save',
      type:'POST',
      data:{ id:wineID }
    })
  })
});
