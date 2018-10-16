function check_if_mobile(){

  var res = false;
  var width = $(window).width();

  if(width <= 992)
  {
    if (!$("body").hasClass("menu_mobile_padding"))
      $("body").addClass("menu_mobile_padding");
    res = true
  }
  else
  {
    if ($("body").hasClass("menu_mobile_padding"))
      $("body").removeClass("menu_mobile_padding");
    res = false
  }

  return res
}
