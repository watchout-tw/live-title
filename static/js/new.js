
function init_new(){
  app_init();
}

function app_init(){
  // create a root instance
  var app =new Vue({
    el: '#app',
    data:{
      state_init: true,
      folder_url: "",
      folder_check: false,
      folder_title: "",
      folder_owner:"",
      error: false,
      msg:"",
      state_mobile_menu: false,
      mobile:check_if_mobile()
    },
    created: function () {
      window.addEventListener('resize', this.handleResize);
    },
    updated: function () {
    },
    methods: {
      handleResize (event) {
          app.$data.mobile = check_if_mobile();
      },
      check_url:function (url){
        //window.open(link);
      },
      check_email:function (mail){

      },
      create: function () {
        var url = "/new";
        var f_url = "";
        var f_email = "";
        var f_title = "";
        var f_description = "";
        var f_cover = "";

        f_url = $('#f_url').val();
        f_email = $('#f_email').val();
        f_title = $('#f_title').val();
        f_description = $('#f_description').val();
        f_cover = $('#f_cover').val();


        $.ajax({
          type: "POST",
          url: url,
          data: {
            'f_url': f_url,
            'f_email': f_email,
            'f_title': f_title,
            'f_description': f_description,
            'f_cover': f_cover
          },
          dataType: 'JSON',
          success: function(msg){
            app.$data.error = false;
            alert(msg);
          },
          error:function(xhr, ajaxOptions, thrownError){
            app.$data.error = true;
            app.$data.msg = xhr.responseText;
          }
        });
      }
    } // methods
  });
  console.log("Watchout Folders");
}
