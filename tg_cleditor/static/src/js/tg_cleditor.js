openerp.tg_cleditor = function (instance) {
    var QWeb = instance.web.qweb,
        _t =  instance.web._t,
        _lt = instance.web._lt;
   
   var module = instance.tg_cleditor;
   
   module.cleditor = instance.web.form.FieldTextHtml.include({
   
        init: function() {
            this._super.apply(this, arguments);
        },
        initialize_content: function() {
            var self = this;

            if (! this.get("effective_readonly")) {
                self._updating_editor = false;
                this.$textarea = this.$el.find('textarea');
                
                var e_width = ((this.node.attrs || {}).editor_width || '100%');

                var e_height = ((this.node.attrs || {}).editor_height || 250);

                var e_controls = ((this.node.attrs || {}).editor_controls || 
                                "bold italic underline strikethrough " +
                                "| removeformat | bullets numbering | outdent " +
                                "indent | link unlink | source"
                                );

                var e_colors = ((this.node.attrs || {}).editor_colors || 
                                "FFF FCC FC9 FF9 FFC 9F9 9FF CFF CCF FCF " +
                                "CCC F66 F96 FF6 FF3 6F9 3FF 6FF 99F F9F " +
                                "BBB F00 F90 FC6 FF0 3F3 6CC 3CF 66C C6C " +
                                "999 C00 F60 FC3 FC0 3C0 0CC 36F 63F C3C " +
                                "666 900 C60 C93 990 090 399 33F 60C 939 " +
                                "333 600 930 963 660 060 366 009 339 636 " +
                                "000 300 630 633 330 030 033 006 309 303"
                                );

                var e_fonts =((this.node.attrs || {}).editor_fonts ||
                                "Arial,Arial Black,Comic Sans MS,Courier New,Narrow,Garamond," +
                                "Georgia,Impact,Sans Serif,Serif,Tahoma,Trebuchet MS,Verdana"
                                );

                var e_sizes = ((this.node.attrs || {}).editor_sizes || "1,2,3,4,5,6,7");

                var e_docType = ((this.node.attrs || {}).editor_docType || 
                                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'
                                );

                var e_styles =  [["Paragraph", "<p>"], ["Header 1", "<h1>"], ["Header 2", "<h2>"],
                                ["Header 3", "<h3>"],  ["Header 4","<h4>"],  ["Header 5","<h5>"],
                                ["Header 6","<h6>"]];
                                
                if((this.node.attrs || {}).editor_styles) {
                    var es = ((this.node.attrs || {}).editor_styles.split(';')) ; 
                    
                    console.log(es);
                    
                     e_styles = [];
                     for(var i = 0, len = es.length; i < len; i++){
                         e_styles.push(es[i].split(','));
                     }; 
                };

                var e_useCSS = true ;
                            
                            if((this.node.attrs || {}).editor_useCSS){
                                console.log('editor_useCSS : ' + (this.node.attrs || {}).editor_useCSS);
                                if((this.node.attrs || {}).editor_useCSS == "true" ){
                                    e_useCSS = true;
                               }
                            } 

                var e_docCSSFile = ((this.node.attrs || {}).editor_docCSSFile|| "");

                var e_bodyStyle = ((this.node.attrs || {}).editor_bodyStyle || 
                                "margin:4px; color:#4c4c4c; font-size:13px; " +
                                "font-family:'Lucida Grande',Helvetica,Verdana, " + 
                                "Arial,sans-serif; cursor:text"
                                );

                this.$textarea.cleditor({
                        width:        e_width,
                        height:       e_height,
                        controls:     e_controls,
                        colors:       e_colors,    
                        fonts:        e_fonts,
                        sizes:        e_sizes,
                        docType:      e_docType,
                        styles:       e_styles,
                        useCSS:       e_useCSS,
                        docCSSFile:   e_docCSSFile, 
                        bodyStyle:    e_bodyStyle,
                });
                
                this.$cleditor = this.$textarea.cleditor()[0];
                this.$cleditor.change(function() {
                    if (! self._updating_editor) {
                        self.$cleditor.updateTextArea();
                        self.internal_set_value(self.$textarea.val());
                    }
                });
                if (this.field.translate) {
                    var $img = $('<img class="oe_field_translate oe_input_icon" src="/web/static/src/img/icons/terp-translate.png" width="16" height="16" border="0"/>')
                        .click(this.on_translate);
                    this.$cleditor.$toolbar.append($img);
                }
            }
        },
    });
    
};