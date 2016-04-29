var gulp = require('gulp');
var sass = require('gulp-sass');
var csso = require('gulp-csso');
var autoprefixer = require('gulp-autoprefixer');

gulp.task('css', function() {
	gulp.src('admin/css/bootstrap.scss')
		.pipe(sass())
		.pipe(csso())
		.pipe(autoprefixer({
			browsers: ['last 2 versions'],
			cascade: false
		}))			
		.pipe(gulp.dest('./admin/css'));
});

gulp.task('watch', function() {	
	gulp.watch(['admin/css/bootstrap.scss'], ['css']);	
});

gulp.task('default', ['css', 'watch']);