$(document).ready(function () {
  $('.sidenav').sidenav({
    edge: 'right'
  });
  $('.tooltipped').tooltip();
  $('.fixed-action-btn').floatingActionButton();
  $('.parallax').parallax();
  $('.modal').modal();
  $('.collapsible').collapsible();

  $('.carousel').carousel({
    fullWidth: true,
    // dist: 0,
    indicators: true,
  });
  setInterval(function () {
    $('.carousel').carousel('next');
  }, 5000);

  $('#id_details').addClass('materialize-textarea');
  $('#id_due_date').addClass('datepicker');
  $('#id_date').addClass('datepicker');

  const date = new Date($('#id_due_date').val());
  $('.datepicker').datepicker({
    autoClose: true,
    // defaultDate: date,
    setDefaultDate: true,
  });

  moveDealPlatformBtn();
  $(window).scroll(function () {
    moveDealPlatformBtn();
  });

  function moveDealPlatformBtn() {
    if ($(document).scrollTop() > 100) {
      $('.add-deal-btn-top').addClass('scale-out');
      $('.add-deal-btn-top').removeClass('scale-in');
      $('.add-deal-btn-bottom').addClass('scale-in');
      $('.add-deal-btn-bottom').addClass('scale-out');

      $('.add-platform-btn-top').addClass('scale-out');
      $('.add-platform-btn-top').removeClass('scale-in');
      $('.add-platform-btn-bottom').addClass('scale-in');
      $('.add-platform-btn-bottom').addClass('scale-out');
    }
    else {
      $('.add-deal-btn-top').addClass('scale-in');
      $('.add-deal-btn-top').removeClass('scale-out');
      $('.add-deal-btn-bottom').addClass('scale-out');
      $('.add-deal-btn-bottom').removeClass('scale-in');

      $('.add-platform-btn-top').addClass('scale-in');
      $('.add-platform-btn-top').removeClass('scale-out');
      $('.add-platform-btn-bottom').addClass('scale-out');
      $('.add-platform-btn-bottom').removeClass('scale-in');
    }
  }
});