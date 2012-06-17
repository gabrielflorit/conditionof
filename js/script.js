/* Author: Gabriel Florit */

var conditionOf = (function () {

	return {

		// resetBar: function(markerCenter) {
		// },

		// bar: null
	}

}());

$(function() {

	// create codemirror instance
	conditionOf.codeMirror = CodeMirror($('#poem').get(0), {

		mode:  'javascript',

		onCursorActivity: function(cm) {

			var cursor = cm.getCursor();
			var token = cm.getTokenAt(cursor);
			$('#test').text(token.string);

		}
	});

	// load all the reasons in memory
	var reasons = [
		'for fear of alienating a landlord.',
		'because of fears that he too could be kidnapped.',
		'because the subject is politically sensitive.',
		'because she lives alone'
	];

	conditionOf.codeMirror.setValue('for fear of alienating a landlord.\nbecause of fears that he too could be kidnapped.\n');

});






