$(document).ready(function () {
  $('.parallax').parallax();

  $('#id_details').addClass('materialize-textarea');
  $('#id_due_date').addClass('datepicker');

  const date = new Date($('#id_due_date').val());
  $('.datepicker').datepicker({
    autoClose: true,
    defaultDate: date,
    setDefaultDate: true,
  });
  
  $('.modal').modal();
});