/* Author: Gabriel Florit */

var conditionOf = (function () {

	return {

		createLines: function(reasons) {

			var theString = '';

			_.each(reasons, function(value, key, list) {
				theString += value.reason + '\n';
			});

			return theString;
		},

		clickToken: function() {

			var cursor = conditionOf.codeMirror.getCursor();
			var token = conditionOf.codeMirror.getTokenAt(cursor);
			var word = token.string;

			// find reasons containing this word
			var newReasons = _.filter(conditionOf.reasons, function(reason) {
				return reason.reason.indexOf(word) != -1;
			});

			conditionOf.codeMirror.setValue(conditionOf.createLines(newReasons));
		},

		reasons: null
	}

}());

$(function() {

	// create codemirror instance
	conditionOf.codeMirror = CodeMirror($('#poem').get(0), {

		mode:  'javascript',

	});

	$('#poem').on('click', function(e) {
		console.log('click');
		conditionOf.clickToken();
	});

	// load all the reasons in memory
	var reasons = d3.json('js/data/reasons.json', function(data) {

		conditionOf.reasons = data;
		conditionOf.codeMirror.setValue(conditionOf.createLines(data));

	});

});






