var gulp       = require('gulp'),
    gutil      = require('gutil'),
    sass       = require('gulp-sass'),
    coffee     = require('gulp-coffee'),
    rename     = require('gulp-rename'),
    sourcemaps = require('gulp-sourcemaps'),
    compress   = require('gulp-yuicompressor'),
    concat     = require('gulp-concat-sourcemap'),
    shell      = require('gulp-shell');

var DEBUG  = true;

var paths = {
    'sass'   : './sass/**/*.sass',
    'coffee' : './coffee/**/*.coffee'
};

var separateJsFiles = [
    'js/html5shiv.min.js', 'js/respond.min.js',
    'js/jquery-1.12.4.min.js', 'js/jquery-2.2.4.min.js'
];

/**
 * Add js files here for compress and concatenate
 */
var concatenatedJsFiles = [
    'js/main.js'
];

/**
 * Add css files here for compress and concatenate
 */
var concatenatedCssFiles = [
    'css/font-awesome.min.css',
    'css/normalize.css',
    'css/main.css'
];

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

gulp.task('css-concat', function () {
    gulp.src(concatenatedCssFiles)
        .pipe(concat('styles.min.css', {
            sourcesContent : DEBUG
        }))
        .pipe(gulp.dest('css'));
});

gulp.task('coffee', function () {
    var pipe = gulp.src(paths.coffee);
    if (DEBUG) {
        pipe = pipe.pipe(sourcemaps.init());
    }
    pipe = pipe.pipe(coffee({
        bare: true
    })).on('error', errHandler);
    if (DEBUG) {
        pipe = pipe.pipe(sourcemaps.write());
    }
    pipe.pipe(gulp.dest('js'));
});

gulp.task('js-concat', function () {
    gulp.src(concatenatedJsFiles)
        .pipe(concat('app.min.js', {
            sourcesContent : DEBUG
        }))
        .pipe(gulp.dest('js'));
});

gulp.task('watch', function () {
    gulp.watch(paths.sass, ['sass', 'css-concat']);
    gulp.watch(paths.coffee, ['coffee', 'js-concat']);
});

gulp.task('compile', ['sass', 'coffee']);

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
    gulp.src('bower_components/jquery-legacy/dist/jquery.min.js')
        .pipe(rename('jquery-1.12.4.min.js'))
        .pipe(gulp.dest('js'));
    gulp.src('bower_components/jquery-modern/dist/jquery.min.js')
        .pipe(rename('jquery-2.2.4.min.js'))
        .pipe(gulp.dest('js'));
    gulp.src('bower_components/respond/dest/respond.min.js')
        .pipe(gulp.dest('js'));
    gulp.src('bower_components/html5shiv/dist/html5shiv.min.js')
        .pipe(gulp.dest('js'));
});

/**
 * Minify for build
 */
gulp.task('static-minify', function () {
    console.log('\n\tBuild static files...');
    console.log('\tDEBUG is:', DEBUG, '\n');
    gulp.src('css/styles.min.css')
        .pipe(compress({ type: 'css' }))
        .pipe(gulp.dest('css'));
    gulp.src('js/app.min.js')
        .pipe(compress({ type: 'js' }))
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
gulp.task('pro-compile', ['undebug', 'compile', 'js-concat', 'css-concat']);
gulp.task('pro-build', ['undebug', 'static-minify']);

/**
 * Build task
 */
gulp.task('build', shell.task([
    'gulp copy && gulp pro-compile && gulp pro-build'
]));
