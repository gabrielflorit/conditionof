/* Author: Gabriel Florit */

var conditionOf = (function () {

	return {

		createLines: function(reasons) {

			var lineArray = [];
			var a = 0;

			for (var i = 0; i < reasons.length; i++) {
				lineArray[a++] = reasons[i].reason;
			}

			return lineArray.join('\n');
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
		readOnly: true
	});

	$('#poem').on('click', function(e) {
		conditionOf.clickToken();
	});

	// load all the reasons in memory
	var reasons = d3.json('static/js/data/reasons.json', function(data) {

		conditionOf.reasons = data;
		conditionOf.codeMirror.setValue(conditionOf.createLines(data));

	});

});






