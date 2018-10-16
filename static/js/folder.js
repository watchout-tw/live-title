
var LIST ="";
var INIT_PAGE = "";
var TITLE = "";
var COVER = "";
var ID = "";
function init_folder(target){
  var url = "/data/f/" + target;
  $.getJSON( url, function( data ) {
      if( !data.error || (data.error = undefined))
      {
        console.log(data);
        console.log("!!!");
        LIST = data.list;
        TITLE = data.title;
        COVER = data.cover;
        ID = data.id
        console.log(LIST);
        INIT_PAGE = LIST[0].link;
        console.log(INIT_PAGE);
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
      list_data: LIST,
      id: ID,
      title: TITLE,
      cover: COVER,
      page: INIT_PAGE,
      state_mobile_menu: false,
      mobile:check_if_mobile()
    },
    created: function () {
      $('.collapsible').collapsible();
      //window.addEventListener('resize', this.handleResize);
    },
    updated: function () {
      $('.collapsible').collapsible();
    },
    methods: {
      handleResize (event) {
          app.$data.mobile = check_if_mobile();
      },
      open_page: function (page) {
        app.$data.page = page;
      },
      open_link:function (url){
        window.open(url, '_blank');
      }
    } // methods
  });
  //$('.collapsible').collapsible();
  console.log("Watchout Folders");
}
