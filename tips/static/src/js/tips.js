openerp.tips = function(instance){
	var QWeb = instance.web.qweb,
    	_t =  instance.web._t;

	var module = instance.tips;
	var next_tip = 0;

	var fetch = function(model, fields, domain, ctx){
        return new instance.web.Model(model).query(fields).filter(domain).context(ctx).all();
    };

    var shuffle_array = function(o){ 
    	for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    		return o;
    };

    module.tips = instance.web.ViewManager.include({

    	start: function(){
    		var tmp = this._super.apply(this, arguments);
        	var self = this;        
        	var model = self.dataset.model;

        	self.get_avail_tips(model);
        	return tmp;
    	},

    	get_avail_tips: function(model){
    		var self = this;
    		if($("#tip_tr").length == 0) {
	    		var loaded = fetch('tip',['name', 'texte'],['|', ['model_ids', '=', model], ['model_ids', '=', false], ['active', '=', true]])
	    		.then(function(tips){
                    if(tips.length > 0){
                        next_tip = 0;
	    			    self.render_one_tip(shuffle_array(tips));
                        }				
	    		});
	    	}
    	},

    	render_one_tip: function(tips){
    		var self = this;          
    		if(tips.length > 0){
    			if($("#tip_tr").length == 0 ) {				
    				var tip_tpl = QWeb.render('Tip',{});
            		$(tip_tpl).prependTo($('.oe_view_manager_header').first()); 
            		$('#nb_tips').html(tips.length);

            		$('#img_next').click(function(){
		    			self.render_one_tip(tips);
	    			});  				
		    	}

		    	var n = next_tip + 1 ;
	    		$('.tip_title').html(n + ' - ' + tips[next_tip].name);
	    		$('.tip_text').html(tips[next_tip].texte);

	    		next_tip = next_tip + 1;
	    		if(next_tip >= tips.length){next_tip = 0 };	
	    	}

	    	tips.length > 1 ? $('.tip_next').css('display', 'inline-block') : $('.tip_next').css('display', 'none');

    	},

    });
};