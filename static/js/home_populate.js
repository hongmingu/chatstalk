function home_populate(){
                            var id = $('script').last().parent().attr('data-u')
                            var parent_div = $('script').last().parent()
                            var user_id = $('#user_id').attr('data-u')
                            $(function () {
                                $.ajax({
                                    url: '/re/user/home/populate/', type: 'post', dataType:'json', cache: false,
                                    data: {
                                        post_id: id,
                                    },
                                    success: function (data) {

                                        if (data.res === 1){
                                            var _last_chat;
                                            switch (data.set.last_chat.kind){
                                                case 'start':
                                                    _last_chat = '<span class="home_feed_chat_start">'+'Conversation started'+'</span>'
                                                    break;
                                                case 'text':
                                                    if (data.set.you_say === true){
                                                        _last_chat = '<span>'+data.set.name+'</span><span><b>: </b></span>'+'<span class="home_feed_chat_text">'+data.set.last_chat.text+'</span>'
                                                    } else {
                                                        _last_chat = '<span class="home_feed_chat_text">'+data.set.last_chat.text+'</span>'
                                                    }
                                                    break;

                                                case 'photo':
                                                    if (data.set.you_say === true){
                                                        _last_chat = '<span>'+data.set.name+'</span><span><b>: </b></span>'+'<span class="home_feed_chat_photo">'+'photo'+'</span>'
                                                    } else {
                                                        _last_chat = '<span class="home_feed_chat_photo">'+'photo'+'</span>'
                                                    }
                                                    break;
                                                default:
                                                    _last_chat = '<span class="home_feed_chat_start">'+'Conversation?'+'</span>'
                                                    break;
                                            }
                                            var _title ,_title_class, _desc, _desc_class
                                            if (data.set.title === null){
                                                _title_class = ' hidden'
                                                _title = ''
                                            } else {
                                                _title_class = ''
                                                _title = data.set.title
                                            }
                                            if (data.set.desc === null){
                                                _desc_class = ' hidden'
                                                _desc = ''
                                            } else {
                                                _desc_class = ''
                                                _desc = data.set.desc
                                            }
                                            var _comment = '';
                                            var _last_comment_id = '';
                                            if (data.set.three_comments !== null){
                                                $.each(data.set.three_comments, function (key, value) {
                                                    var _remove;
                                                    if(value.comment_user_id===user_id){
                                                        _remove = '<a href=""><span class="glyphicon glyphicon-remove home_feed_comment_delete clickable" data-u="'+value.comment_uuid+'"></span></a>'
                                                    }
                                                    _comment = _comment + '<div id="comment_div_'+value.comment_uuid+'"><div><a href="#"><span class="comments_name">'+value.comment_username+'</span></a></div><div><span class="comments">'+value.comment_text+'</span>   <span class="home_feed_comment_time">'+date_differ(value.comment_created)+'</span> '+_remove+'</div></div>'
                                                    _last_comment_id = value.comment_uuid
                                                })
                                            }
                                            var _more_comments_class = '';
                                            if (data.set.comment_count < 4){
                                                _more_comments_class = 'hidden'
                                            }
                                            var _like = ' glyphicon-heart-empty ';
                                            if (data.set.you_liked === true){
                                                _like = ' glyphicon-heart '
                                            }
                                            var _new = '';
                                            if (data.set.new === true){
                                                _new = '<div class="home_feed_chat_new" align="center">new</div>'
                                            }
                                            // 제목에 공백만 있는 건 허용하지 말자. 자바스크립트로. 그렇게 하고 파이썬 뷰에서 그렇게 하자.
                                            var append_to = $('<div class="media">\n' +
                                                '<div class="media-heading margin_bottom_30">\n' +
                                                '<div class="col-xs-10 padding_left_0" align="left"><span\n' +
                                                'class="home_feed_name">'+data.set.username+'</span></div>\n' +
                                                '<div class="col-xs-2" align="right">\n' +
                                                '<a href="#"><span\n' +
                                                'class="glyphicon glyphicon-option-horizontal grey"></span></a></div>\n' +
                                                '</div>\n' +
                                                '<a href=""><div id="chat_div_'+data.set.id+'" class="home_feed_chat_total">'+
                                                '<div class="media-left">\n' +
                                                '<img src="'+data.set.photo+'"\n' +
                                                'class="media-object img_small">\n' +
                                                '</div>\n' +
                                                '<div class="media-body">\n' +
                                                '<div class="home_feed_chat">'+_last_chat+'</div>' + _new +
                                                '</div>\n' +
                                                '</div></a>\n' +
                                                '<div class="home_feed_title '+ _title_class +'">'+_title+'</div>\n' +
                                                '<div class="home_feed_desc '+ _desc_class +'">'+ _desc+'</div>\n' +
                                                '<div class="media-bottom"><br/>\n' +
                                                '<div class="col-xs-5" align="left"><span\n' +
                                                'class="glyphicon glyphicon-heart heart_black"></span> <span class="home_feed_like_count" id="basic_heart_'+data.set.id+'">'+data.set.like_count+'</span></div>\n' +
                                                '<div class="col-xs-5" align="right"><span class="home_feed_time">'+date_differ(data.set.created)+'</span>\n' +
                                                '</div>\n' +
                                                '<div class="col-xs-2" align="right"><a href="#"><span class="glyphicon'+_like+'heart" id="like_'+data.set.id+'"></span></a></div>\n' +
                                                '<div class=""><span class="comments_title">Comments '+data.set.comment_count+'</span></div>\n' +
                                                '<div class="comments_list" id="comment_list_'+id+'">'+_comment+'</div>\n' +
                                                '<a href="#"><div class="home_feed_comment_more clickable '+_more_comments_class+'" align="center" id="more_comments_'+data.set.id+'">more comments</div></a>\n' +
                                                '</div>\n' +
                                                '</div>\n' +
                                                '<div class="hidden" id="last_comment_'+data.set.id+'" data-u="'+_last_comment_id+'">'+_last_comment_id+'</div>'+
                                                '<div align="center">\n' +
                                                '<form class="padding_top_5">\n' +
                                                '<div class="input-group input-group-sm home_feed_comment_wrapper">\n' +
                                                '<textarea class="form-control home_feed_comment_textarea" id="textarea_'+id+'" placeholder="comment" id="comment_textarea"></textarea>\n' +
                                                '<div class="input-group-btn">\n' +
                                                '<button class="btn btn-default home_feed_comment_textarea_send" id="btn_comment_'+id+'"><i\n' +
                                                'class="glyphicon glyphicon-send"></i></button>\n' +
                                                '</div>\n' +
                                                '</div>\n' +
                                                '</form>\n' +
                                                '</div>')

                                            append_to.find('#chat_div_'+data.set.id).on('click', function (e) {
                                                e.preventDefault()
                                                $('#reading_post_id').html(data.set.id)
                                                $('#reading_post_profile_photo').html(data.set.photo)
                                                $('#reading_post_profile_name').html(data.set.name)
                                                $('#reading_post_user_id').html(data.set.user_id)
                                                $('#modal_reading_post').modal('show')
                                            })
                                            append_to.find('#like_'+data.set.id).on('click', function (e) {
                                                e.preventDefault()
                                                $.ajax({url:'/re/post/like/', type:'post', dataType:'json', cache:false,
                                                    data:{
                                                        post_id:data.set.id,
                                                    },
                                                    success:function (sub_data) {
                                                    console.log(sub_data)
                                                        if (sub_data.res === 1) {
                                                            var current_count = parseInt($('#basic_heart_'+data.set.id).html())
                                                            if (sub_data.liked === true){
                                                                if ($('#like_'+data.set.id).hasClass('glyphicon-heart-empty')){
                                                                    $('#like_'+data.set.id).removeClass('glyphicon-heart-empty')
                                                                    $('#like_'+data.set.id).addClass('glyphicon-heart')
                                                                }
                                                                $('#basic_heart_'+data.set.id).html(current_count + 1)
                                                            } else if (sub_data.liked === false){
                                                                if ($('#like_'+data.set.id).hasClass('glyphicon-heart')){
                                                                    $('#like_'+data.set.id).removeClass('glyphicon-heart')
                                                                    $('#like_'+data.set.id).addClass('glyphicon-heart-empty')
                                                                }
                                                                $('#basic_heart_'+data.set.id).html(current_count - 1)
                                                            }


                                                        }
                                                    }
                                                })
                                            })
                                            //이제 대화 모달이랑 그다음 포스트메뉴 모달 만들고 프로필창 만들고 .
                                            append_to.find('.home_feed_comment_delete').on('click', function (e) {
                                                e.preventDefault()
                                                var deleted_id = $(this).attr('data-u')
                                                $.ajax({url:'/re/comment/delete/', type:'post', dataType:'json', cache:false,
                                                    data:{
                                                        post_id:id,
                                                        comment_id:deleted_id,
                                                    },
                                                    success:function (sub_data) {
                                                    console.log(sub_data)
                                                        if (sub_data.res === 1) {
                                                            $('#comment_div_'+deleted_id).replaceWith('<div>removed</div>')
                                                        }
                                                    }
                                                })
                                            })
                                            append_to.find('#textarea_'+id).on('keypress', function (e) {
                                                if (e.keyCode == 13 && !e.shiftKey) {
                                                    var text = $('#textarea_'+id).val()
                                                    if (text === '') {
                                                        return false;
                                                    } else if (1<=text.length && text.length<=1000) {
                                                        $.ajax({url:'/re/comment/add/', type:'post', dataType:'json', cache:false,
                                                            data:{
                                                                post_id:id,
                                                                comment:text,
                                                            },
                                                            success:function (data) {
                                                            console.log(data)
                                                                if (data.res === 1) {
                                                                    var _comment = '';
                                                                    if (data.set !== null){
                                                                        $.each(data.set, function (key, value) {
                                                                            var _remove;
                                                                            if(value.comment_user_id===user_id){
                                                                                _remove = '<a href=""><span class="glyphicon glyphicon-remove home_feed_comment_delete clickable" data-u="'+value.comment_uuid+'"></span></a>'
                                                                            }
                                                                            _comment = '<div class="home_feed_new_comment" id="comment_div_'+value.comment_uuid+'"><div><a href="#"><span class="comments_name">'+value.comment_username+'</span></a></div><div><span class="comments">'+value.comment_text+'</span>   <span class="home_feed_comment_time">'+date_differ(value.comment_created)+'</span> '+_remove+'</div></div>'
                                                                        })
                                                                    }
                                                                    var _comment_prepender = $(_comment)
                                                                    _comment_prepender.find('.home_feed_comment_delete').on('click', function (e) {
                                                                        e.preventDefault()
                                                                        var deleted_id = $(this).attr('data-u')
                                                                        $.ajax({url:'/re/comment/delete/', type:'post', dataType:'json', cache:false,
                                                                            data:{
                                                                                post_id:id,
                                                                                comment_id:deleted_id,
                                                                            },
                                                                            success:function (data) {
                                                                            console.log(data)
                                                                                if (data.res === 1) {
                                                                                    $('#comment_div_'+deleted_id).replaceWith('<div>removed</div>')
                                                                                }
                                                                            }
                                                                        })
                                                                    })
                                                                    $('#comment_list_'+id).prepend(_comment_prepender)
                                                                    $('#textarea_'+id).val('')
                                                                }
                                                            }
                                                        })
                                                    }
                                                    else if ( 1000< text.length){
                                                        alert('too long')
                                                    }
                                                }
                                            })

                                            append_to.find('#btn_comment_'+id).on('click', function (e) {
                                                e.preventDefault()
                                                var text = $('#textarea_'+id).val()
                                                if (text === '') {
                                                    return false;
                                                }
                                                else if (1<=text.length && text.length<=1000) {
                                                    $.ajax({url:'/re/comment/add/', type:'post', dataType:'json', cache:false,
                                                        data:{
                                                            post_id:id,
                                                            comment:text,
                                                        },
                                                        success:function (data) {
                                                        console.log(data)
                                                            if (data.res === 1) {
                                                                var _comment = '';
                                                                if (data.set !== null){
                                                                    $.each(data.set, function (key, value) {
                                                                        var _remove;
                                                                        if(value.comment_user_id===user_id){
                                                                            _remove = '<a href=""><span class="glyphicon glyphicon-remove home_feed_comment_delete clickable" data-u="'+value.comment_uuid+'"></span></a>'
                                                                        }
                                                                        _comment = '<div class="home_feed_new_comment" id="comment_div_'+value.comment_uuid+'"><div><a href="#"><span class="comments_name">'+value.comment_username+'</span></a></div><div><span class="comments">'+value.comment_text+'</span>   <span class="home_feed_comment_time">'+date_differ(value.comment_created)+'</span> '+_remove+'</div></div>'
                                                                    })
                                                                }
                                                                var _comment_prepender = $(_comment)
                                                                _comment_prepender.find('.home_feed_comment_delete').on('click', function (e) {
                                                                    e.preventDefault()
                                                                    var deleted_id = $(this).attr('data-u')
                                                                    $.ajax({url:'/re/comment/delete/', type:'post', dataType:'json', cache:false,
                                                                        data:{
                                                                            post_id:id,
                                                                            comment_id:deleted_id,
                                                                        },
                                                                        success:function (data) {
                                                                        console.log(data)
                                                                            if (data.res === 1) {
                                                                                $('#comment_div_'+deleted_id).replaceWith('<div>removed</div>')
                                                                            }
                                                                        }
                                                                    })
                                                                })
                                                                $('#comment_list_'+id).prepend(_comment_prepender)
                                                                $('#textarea_'+id).val('')
                                                            }
                                                        }
                                                    })
                                                }
                                                else if ( 1000< text.length){
                                                    alert('too long')
                                                }

                                            })

                                            append_to.find('#more_comments_'+data.set.id).on('click', function (e) {
                                                e.preventDefault()
                                                $.ajax({url:'/re/comment/more/load/', type:'post', dataType:'json', cache:false,
                                                    data:{
                                                        post_id:id,
                                                        last_comment_id:$('#last_comment_'+data.set.id).html(),
                                                    },
                                                    success:function (sub_data) {
                                                    console.log(sub_data)
                                                        if (sub_data.res === 1) {
                                                            var _comment = '';
                                                            if (sub_data.set !== null){
                                                                $.each(sub_data.set, function (key, value) {

                                                                    var _remove;
                                                                    if(value.comment_user_id===user_id){
                                                                        _remove = '<a href=""><span class="glyphicon glyphicon-remove home_feed_comment_delete clickable" data-u="'+value.comment_uuid+'"></span></a>'
                                                                    }
                                                                    _comment = _comment + '<div id="comment_div_'+value.comment_uuid+'"><div><a href="#"><span class="comments_name">'+value.comment_username+'</span></a></div><div><span class="comments">'+value.comment_text+'</span>   <span class="home_feed_comment_time">'+date_differ(value.comment_created)+'</span> '+_remove+'</div></div>'
                                                                    $('#last_comment_'+data.set.id).html(value.comment_uuid)
                                                                    //이제 end 일 경우 hidden 붙이는거랑 삭제 구현하자.
                                                                })
                                                            }
                                                            var _comment_appender = $(_comment)
                                                            _comment_appender.find('.home_feed_comment_delete').on('click', function (e) {
                                                                e.preventDefault()
                                                                var deleted_id = $(this).attr('data-u')
                                                                $.ajax({url:'/re/comment/delete/', type:'post', dataType:'json', cache:false,
                                                                    data:{
                                                                        post_id:id,
                                                                        comment_id:deleted_id,
                                                                    },
                                                                    success:function (data) {
                                                                    console.log(data)
                                                                        if (data.res === 1) {
                                                                            $('#comment_div_'+deleted_id).replaceWith('<div>removed</div>')
                                                                        }
                                                                    }
                                                                })
                                                            })
                                                            $('#comment_list_'+id).append(_comment_appender)
                                                            if (sub_data.end === true){
                                                                if (!($('#more_comments_'+data.set.id).hasClass('hidden'))){
                                                                    $('#more_comments_'+data.set.id).addClass('hidden')
                                                                }
                                                            }

                                                        }
                                                    }
                                                })
                                            })

                                            $('#div_').append(append_to)
                                        }
                                    }
                                })
                            })
                        }