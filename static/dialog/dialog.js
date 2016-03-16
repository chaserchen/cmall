veil.event.EVENT_DIALOG_INIT = "init.dialog";
veil.event.EVENT_DIALOG_CLOSING = "closing.dialog";

(function($) {
    var settings = {
        cache: undefined,
        model: false,
        showClose: true,
        content: '',
        width: 'auto',
        height: 'auto',
        left: '',
        right: '',
        top: '',
        draggable: false,
        setFocus: false,
        beforeShow: function (dialog) {
        },
        onShown: function (dialog) {
        },
        onClosed: function () {
        }
    };
    $.showDialog = function(options) {

        var _DIALOG_BOX_TEMPLATE = '<div id="dialog-box" style="display:none"><img id="dialog-close-button" src="/static/dialog/dialog-close.gif"><div id="dialog-box-content"></div> </div>';

        if (options) {
            $.extend(settings, options);
        }

        showOverlay();
        showDialogBox();
        bindEventHandler();
        if (settings.setFocus) {
            setFocus();
        }

        function showOverlay() {
            if ($('#dialog-overlay').length == 0) {
                $('body').append('<div id="dialog-overlay" style="display:none"></div>');
            }
            setOverlaySize();
            $('#dialog-overlay').show();
        }

        function showDialogBox() {
            if ($('#dialog-box').length == 0) {
                $('body').append(_DIALOG_BOX_TEMPLATE);
            }
            prepareDialogContent();
            locateDialogBox();
            showCloseButton();
            if (settings.draggable) {
                $('#dialog-box').draggable();
            }

            veil.event.publish(veil.event.EVENT_DIALOG_INIT);

            settings.beforeShow($('#dialog-box'));

            $('#dialog-box').fadeIn(500, function() {
                settings.onShown($('#dialog-box'));
            });
        }

        function setFocus(){
            $("#dialog-box-content input:enabled:text:visible:first").focus();
        }

        function prepareDialogContent() {
            var dialogBoxContent = $('#dialog-box-content');

            var content = getDialogContent();
            dialogBoxContent.html(content);
        }

        function getDialogContent() {
            var content = settings.content;
            if (content.jquery) {
                return content;
            } else if (settings.content.match(/^\//)) {
                content = getContentByAjax(settings.content);
            } else if (settings.content.match(/^#/)) {
                var locator = settings.content;
                content = $(locator);
                content.show();
            }
            return content;
        }

        function getContentByAjax(url) {
            var content = '';
            var _ = {
                url: url,
                async:false,
                success:function(payload) {
                    content = payload;
                },
                statusCode:{
                    403:function (xhr) {
                        content = xhr.responseText;
                    }
                }
            };
            if (settings.cache !== undefined) {
                _.cache = settings.cache;
            }
            $.ajax(_);
            return content;
        }

        function showCloseButton() {
            if (settings.showClose) {
                $('#dialog-close-button').show();
            }
            else {
                $('#dialog-close-button').hide();
            }
        }

        function locateDialogBox() {
            var dialogBox = $('#dialog-box');
            setDialogBoxSize(dialogBox);
            positionDialogBox(dialogBox);
        }
        function positionDialogBox(dialogBox){
            if(noSpecifiedPosition()){
                stayCenter(dialogBox);
            }
            else{
                stayAtSpecifiedPosition(dialogBox);
            }
        }
        function noSpecifiedPosition(){
            return settings.top==='';
        }
        function stayCenter(dialogBox){
            var top = $(document).scrollTop() + ($(window).height() - dialogBox.height()) / 2;
            var left = ($(window).width() - dialogBox.width()) / 2;
            dialogBox.css({left: left, top: top});
        }
        function stayAtSpecifiedPosition(dialogBox){
            var top = settings.top - dialogBox.height()/2;
            if(top< 20){
                top = ($(window).height() - dialogBox.height()) / 3;
            }
            
            if(settings.left !==''){
                dialogBox.css({left: settings.left, top: top});
            } else if(settings.right !==''){
                dialogBox.css({left: settings.right - dialogBox.outerWidth(), top: top});
            }else{
                alert("Must assign left/right position when popup dialog defined top position.");
            }
        }

        function setDialogBoxSize(dialogBox) {
            dialogBox.css('width', settings.width);
            dialogBox.css('height', settings.height);
        }

        function setOverlaySize() {
            var overlay = $('#dialog-overlay');
            overlay.width(getDocWidth());
            overlay.height(getDocHeight());
        }
        function getDocWidth() {
            var D = document;
            return Math.max(
                Math.max(D.body.scrollWidth, D.documentElement.scrollWidth),
                Math.max(D.body.offsetWidth, D.documentElement.offsetWidth),
                Math.max(D.body.clientWidth, D.documentElement.clientWidth)
            );
        }
        function getDocHeight() {
            var D = document;
            return Math.max(
                Math.max(D.body.scrollHeight, D.documentElement.scrollHeight),
                Math.max(D.body.offsetHeight, D.documentElement.offsetHeight),
                Math.max(D.body.clientHeight, D.documentElement.clientHeight)
            );
        }
        function bindEventHandler() {
            bindWindowResizeEventHandler();
            bindCloseEventHandler();
        }

        function bindWindowResizeEventHandler() {
            $(window).resize(function() {
                setOverlaySize();
//                centerDialogBox();
            });
        }

        function bindCloseEventHandler() {
            if (!settings.model) {
                $('#dialog-overlay').click(function() {
                    $.closeDialog();
                });
            }
            $(document).on('click', '#dialog-close-button, .close-dialog', function() {
                $.closeDialog();
            });

        }
    };
    $.closeDialog = function () {
        veil.event.publish(veil.event.EVENT_DIALOG_CLOSING);
        $('#dialog-box').fadeOut(500, function () {
            "use strict";
            settings.onClosed();
        });
        $('#dialog-overlay').fadeOut(500);
    };
})(jQuery);

(function($) {
    $.confirm = function(options) {
        var settings = {
            message: 'Are you sure?',
            ok: function() {},
            cancel: function() {}
        };
        if (options) {
            $.extend(settings, options);
        }
        
        veil.event.subscribe(veil.event.EVENT_DIALOG_INIT, onLoaded);
        veil.event.subscribe(veil.event.EVENT_DIALOG_CLOSING, onCancel);
        
        var content = '<img src="/static/dialog/dialog-warning.gif"><p class="confirm-content">' + settings.message + '</p><fieldset><button id="confirm-ok">确定</button><button id="confirm-cancel">取消</button></fieldset>';
        $.showDialog({
            content: content,
            model: true,
            width: '300px'
        });

        function onLoaded() {
            $('#confirm-ok').click(function() {
                settings.ok();
                $.closeDialog();
            });
            $('#confirm-cancel').click(function() {
                settings.cancel();
                $.closeDialog();
            });
        }
        function onCancel(){
            settings.cancel();
        }
    }
})(jQuery);

(function($) {
    $.alert = function(options) {
        var settings = {
            message: 'Alert!',
            ok: function() {}
        };
        if (options) {
            $.extend(settings, options);
        }

        veil.event.subscribe(veil.event.EVENT_DIALOG_INIT, onLoaded);
        veil.event.subscribe(veil.event.EVENT_DIALOG_CLOSING, onCancel);

        var content = '<img src="/static/dialog/dialog-warning.gif">' +
            '<p class="confirm-content">' + settings.message + '</p>' +
            '<fieldset>' +
                '<button id="confirm-ok">OK</button>' +
            '</fieldset>';
        $.showDialog({
            content: content,
            model: true,
            width: '300px'
        });

        function onLoaded() {
            $('#confirm-ok').click(function() {
                settings.ok();
                $.closeDialog();
            });
        }
        function onCancel(){
            settings.cancel();
        }
    }
})(jQuery);


POPUP_AT_LEFT='left';
POPUP_AT_RIGHT='right';

(function($) {
    $.popup = function(trigger, content, at) {
        var position = calculatePosition();
        $.showDialog({
            content: content,
            model: false,
            left: position.left,
            right: position.right,
            top: position.top
        });

        function calculatePosition(){
            var left='', right='';

            var top = trigger.position().top + trigger.outerHeight()/2;
            if(at === POPUP_AT_LEFT){
                right = trigger.position().left - 20;
            } else{
                left = trigger.position().left + trigger.outerWidth() + 20;
            }

            return {left: left, top: top, right:right};
        }

    }
})(jQuery);
