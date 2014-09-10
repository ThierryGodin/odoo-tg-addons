openerp.tg_erp_status = function(instance){
	var QWeb = instance.web.qweb,
    	_t =  instance.web._t,
    	_lt = instance.web._lt;

	var module = instance.tg_erp_status;

	module.TgStatus = instance.web.WebClient.include({
		init: function() {
            this._super.apply(this, arguments);

        },

        set_title: function(title) {
            var self = this;
            this._super.apply(this, arguments);

            var uid =  self.session.uid;
            if(uid){
                (new instance.web.Model('tg.erp.status.config')).call('get_erp_status', [])
                    .fail(function(status){
                        alert('Katastroff! : cannot get ERP Status');
                    })
                    .done(function(status){
                        
                        if(status.state == 'maintenance'){
                            if (uid != 1){
                                $('#tg_status_panel').css('display', 'block');
                                $('.openerp_webclient_container').css('overflow', 'hidden');
                                $('#tg_status_panel_frame_text').html(status.message_text);
                            }else{
                                $('#tg_status_frame').css('display', 'block');
                            }
                        }else{
                            $('#tg_status_panel').css('display', 'none');
                            $('#tg_status_frame').css('display', 'none');
                            $('#tg_status_panel_frame_text').html('');
                        }
                    });
            };
    	},

	});

};