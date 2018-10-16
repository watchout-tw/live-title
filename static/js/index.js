var DATA_INDEX ="";

function init_index(){


  var url = "/data/index/1";
  $.getJSON( url, function( data ) {
      if( !data.error || (data.error = undefined))
      {
        DATA_INDEX = data;
        //console.log("DATA Index init!");
        console.log(DATA_INDEX[0]);
        app_init();
      }
  });

}

function app_init(){
  // create a root instance
  var app =new Vue({
    el: '#app',
    data:{
      state_init: true,
      data_index:DATA_INDEX,
      buyaction: null
    },
    created: function () {
      //window.addEventListener('resize', this.handleResize);
      //window.addEventListener('onhashchange', this.test);
    },
    updated: function () {
      init_tools_swiper();
    },
    methods: {
      handleResize (event) {
          app.$data.mobile = check_if_mobile();
      },
      open_link:function (url){
        window.open(url, '_blank');
      },
      open_page:function (url){
        window.open(url);
      },
      open_folder:function (url){
        var link = "/f/"+url;
        window.open(link, '_blank');
      }
    } // methods
  });
  console.log("Watchout Folders");
}
