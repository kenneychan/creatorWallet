$(document).ready(function () {
  $('.parallax').parallax();

  $('#id_details').addClass('materialize-textarea');
  $('#id_due_date').addClass('datepicker');

  $('.datepicker').datepicker();
  $('.modal').modal();
});