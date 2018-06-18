var gulp       = require('gulp'),
    gutil      = require('gutil'),
    sass       = require('gulp-sass'),
    sourcemaps = require('gulp-sourcemaps'),
    shell      = require('gulp-shell');

var DEBUG  = true;

var paths = {
    'sass'   : './sass/**/*.sass'
};

var errHandler = function (err) {
    gutil.log('Error', err);
};


gulp.task('sass', function () {
    var output = DEBUG ? 'expanded' : 'compressed';
    var pipe = gulp.src(paths.sass);
    if (DEBUG) {
        pipe = pipe.pipe(sourcemaps.init());
    }
    pipe = pipe.pipe(sass({ // https://github.com/sass/node-sass#includepaths
        indentWidth : 4,
        outputStyle : output
    }).on('error', errHandler));
    if (DEBUG) {
        pipe = pipe.pipe(sourcemaps.write());
    }
    pipe.pipe(gulp.dest('css'));
});

gulp.task('watch', function () {
    gulp.watch(paths.sass, ['sass']);
});

gulp.task('compile', ['sass']);

/**
 * Development task
 */
gulp.task('default', ['compile', 'watch']);


/**
 * Copy Bower libs
 */
gulp.task('copy', function () {
    console.log('\n\tCopy Bower libraries...\n');
    gulp.src('bower_components/html5-boilerplate/dist/css/normalize.css')
        .pipe(gulp.dest('css'));
    gulp.src('bower_components/font-awesome/css/font-awesome.min.css')
        .pipe(gulp.dest('css'));
    gulp.src('bower_components/font-awesome/fonts/*.*').pipe(gulp.dest('fonts'));
    gulp.src('bower_components/respond/dest/respond.min.js')
        .pipe(gulp.dest('js'));
    gulp.src('bower_components/html5shiv/dist/html5shiv.min.js')
        .pipe(gulp.dest('js'));
});

/**
 * Set DEBUG to false for build
 */
gulp.task('undebug', function () {
    DEBUG = false;
});

/**
 * Subtasks for build
 */
gulp.task('pro-compile', ['undebug', 'compile']);

/**
 * Build task
 */
gulp.task('build', shell.task([
    'gulp copy && gulp pro-compile'
]));
