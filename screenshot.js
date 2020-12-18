//Requires PhantomJS
//Install with apt install phantomjs

var system = require('system');
var args = system.args;

if (args.length === 1) {
  console.log('Try to pass some arguments when invoking this script!');
} else {
  args.forEach(function(arg, i) {
    console.log(i + ': ' + arg);
  });
}
var scriptname=args.shift()
urls=args.slice(1)
// var urls = [
// 		"http://www.google.de",
// 		"http://heise.de",
// 		"https://www.test.de"
// 	]
var	webpage = require('webpage'),
	page = webpage.create(),
  // page.width=1920;
	nr = 0;
  page.viewportSize = {width: 1920, height: 15000};
// Seitendimensionen ggf. anpassen


var screenshot = function() {
	if (!urls.length) phantom.exit();
	var _url = urls.shift();
	console.log('Öffne Seite ' + (nr+1) + ': ' + _url);
	page.open(_url, function(status) {
		if (status !== 'success') {
			console.log('Netzwerkproblem: ' + status);
			urls.unshift(_url);
			setTimeout(screenshot, 1000);
		} else {
			++nr;
			page.evaluate(function() {
				var style = document.createElement('style'),
					bg = document.createTextNode('body {background: #fff}; html {width: 1000px};');
				style.setAttribute('type', 'text/css');
				style.appendChild(bg);
				document.head.insertBefore(style, document.head.firstChild);
			});
			page.render('screenshot_' + nr + '_' + Date.now() + '.jpg', {format: 'jpeg', quality: 80});
			setTimeout(screenshot, 2000);
		}
	});
}

screenshot();
