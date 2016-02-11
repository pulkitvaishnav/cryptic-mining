$(function(){
	$('submit').keypress(function(){
		$.ajax({
			type : 'POST',
			url: '/sparse_matrix/result',
			data: {
				'search_text': $('#search').val(),
				'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val()
			},
			success: searchSuccess,
			dataType: 'html'
		});
	});
});

function searchSuccess(data, textStatus, jqXHR)
{
	$('#search_results').html(data);
}