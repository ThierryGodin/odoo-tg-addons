openerp.tg_box = function(instance){
	var QWeb = instance.web.qweb,
    	_t =  instance.web._t,
    	_lt = instance.web._lt;

	var module = instance.tg_box;

	var fetch = function(model, fields, domain, ctx){
            return new instance.web.Model(model).query(fields).filter(domain).context(ctx).all();
        };

    module.tgboxViewKanban = instance.web_kanban.KanbanView.include({

        do_show: function() {
        	var self = this;
        	this._super();
        	var model = self.dataset.model;
            var allowed_models = new Array();
            allowed_models[0] = 'tg.box';
            var mi = allowed_models.indexOf(model);   
            if(mi >= 0){
                $('.oe_view_manager_view_search').hide();
                $('.tgbox_toolbar').remove();
                $('tr #tgbox_title_comment').remove();
     
                $('.oe_header_row_top').after(QWeb.render("TgBoxView", {widget: this}));
                self.get_cat_description();

                $('.oe_view_manager_body').prepend(QWeb.render("TgSubCatList", {widget: this}));
                self.set_subcat_list();
            }
        },

        set_subcat_list: function(){
        	var self = this;
        	var domain = self.dataset.domain;
        	var cat_id = undefined;
        	
        	for (i = 0; i < domain.length; ++i) {
                if("category_id" == domain[i][0]){
                    cat_id = domain[i][2][0];
                }
            }

            $('.tgbox_toolbar').html('');

            if(cat_id != undefined){
	            (new instance.web.Model('tg.box.category')).call('get_subcat_list', [parseInt(cat_id)])
		        .fail(function(result){
		            alert('Error : cannot get subcat list!');
		        })
		        .done(function(result){
		        	if(result.length > 0) {

		        		for (i = 0; i < result.length; ++i) {
		        			var one_subcat = QWeb.render('TgOneCat', {
		        				subcat_name:result[i].name,
		        			});

		        			$(one_subcat).appendTo($('.tgbox_toolbar')).click(function(){
		        				cur_action_id = this.id;
		        				return self.rpc("/web/action/load", { action_id: cur_action_id}).then(function(result) {
		        					result.flags = result.flags || {};
		        					result.flags.new_window = true;
					                return self.do_action(result, {});
					            });
		        			});
		        			$('.tg_cat_btn:last').attr('id', result[i].action_id);
		        		}
		        	}      
		        });
		    }

        },

        get_cat_description: function(){
            var self = this;
            var domain = self.dataset.domain;
            var cat_id = undefined;

            for (i = 0; i < domain.length; ++i) {
                if("category_id" == domain[i][0]){
                    cat_id = domain[i][2][0];
                }
            }

            if(cat_id != undefined){
                (new instance.web.Model('tg.box.category')).call('read', [cat_id])
                .fail(function(cats){
                    alert('Katastroff! : cannot get cat');
                })
                .done(function(cats){
                    $('.tgbox_comment').html(cats['description']);
                });
            }
        },

    });

	module.tgboxViewForm = instance.web.FormView.include({

		 do_show: function() {  	
        	var tmp = this._super.apply(this, arguments);
        	var self = this;
        	var model = self.dataset.model;
            var allowed_models = new Array();
            allowed_models[0] = 'tg.box';
            var mi = allowed_models.indexOf(model);   
            if(mi >= 0){
                $('.oe_view_manager_view_search').hide();

                if($('.tgbox_toolbar').length > 0){
                	$('.tgbox_toolbar').remove();
                }

                if($('tr #tgbox_title_comment').length > 0){
                	$('tr #tgbox_title_comment').remove();
                }
            }
            return tmp;
        },
	});
};