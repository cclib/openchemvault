from flask_assets import Bundle


def get_assets():
    bundles = {
        'common_css': Bundle(
            'css/ext/bootstrap.min.css',
            'css/thin_scroll.css',
            'css/common.css',
            'css/widgets.css',
            'css/navbar.css',
            output='public/common.css',
            filters='cssmin'),
        'common_js': Bundle(
            'js/ext/jquery.min.js',
            'js/ext/bootstrap.min.js',
            'js/common.js',
            'js/navbar.js',
            output='public/common.js',
            filters='jsmin'),

        'home_css': Bundle(
            'css/home.css',
            output='public/home.css',
            filters='cssmin'),
        'home_js': Bundle(
            'js/home.js',
            output='public/home.js',
            filters='jsmin'),

        'browse_css': Bundle(
            'css/browse.css',
            output='public/browse.css',
            filters='cssmin'),
        'browse_js': Bundle(
            'js/browse.js',
            output='public/browse.js',
            filters='jsmin'),

        'view_css': Bundle(
            'css/view.css',
            output='public/view.css',
            filters='cssmin'),
        'view_js': Bundle(
            'js/view.js',
            output='public/view.js',
            filters='jsmin'),

        'search_css': Bundle(
            'css/search.css',
            output='public/search.css',
            filters='cssmin'),
        'search_js': Bundle(
            'js/search.js',
            output='public/search.js',
            filters='jsmin'),

        'upload_css': Bundle(
            'css/upload.css',
            output='public/upload.css',
            filters='cssmin'),
        'upload_js': Bundle(
            'js/upload.js',
            output='public/upload.js',
            filters='jsmin'),

        'addfile_css': Bundle(
            'css/addfile.css',
            output='public/addfile.css',
            filters='cssmin'),
        'addfile_js': Bundle(
            'js/addfile.js',
            output='public/addfile.js',
            filters='jsmin'),

        '3Dviewer_css': Bundle(
            'css/3Dviewer.css',
            output='public/3Dviewer.css',
            filters='cssmin'),
        '3Dviewer_js': Bundle(
            'js/3Dviewer.js',
            output='public/3Dviewer.js',
            filters='jsmin')
    }
    return bundles
