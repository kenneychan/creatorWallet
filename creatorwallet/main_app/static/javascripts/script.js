$(document).ready(function () {
  $('.parallax').parallax();

  $('.login-field').children('label').each(function () {
    const label = $(this).text().replace(':', '');
    $(this).text(label);
  });
});