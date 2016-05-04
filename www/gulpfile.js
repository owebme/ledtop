var gulp = require('gulp');
var sass = require('gulp-sass');
var csso = require('gulp-csso');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var autoprefixer = require('gulp-autoprefixer');

gulp.task('private_css', function() {
	gulp.src(['js/select2/select2.css',
		'js/datatables/css/bootstrap.css',
		'css/private.css'])
		.pipe(concat('private.min.css'))
		.pipe(sass())
		.pipe(csso())
		.pipe(autoprefixer({
			browsers: ['last 2 versions'],
			cascade: false
		}))			
		.pipe(gulp.dest('./css'));
});

gulp.task('private_libs', function() {
	gulp.src(['js/select2/select2.min.js',
		'js/datatables/jquery.dataTables.min.js',
		'js/datatables/dataTables.bootstrap.js',
		'js/datatables/dataTables.buttons.min.js',
		'js/datatables/buttons.bootstrap.min.js',
		'js/datatables/jszip.min.js',
		'js/datatables/pdfmake.min.js',
		'js/datatables/vfs_fonts.js',
		'js/datatables/buttons.html5.min.js',
		'js/datatables/buttons.print.min.js'])
		.pipe(concat('private.libs.js'))
		.pipe(gulp.dest('./js'));	
});

gulp.task('bootstrap', function() {
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
	gulp.watch(['admin/css/bootstrap.scss'], ['bootstrap']);
	gulp.watch(['css/private.css'], ['private_css']);
});

gulp.task('default', ['private_libs', 'private_css', 'watch']);