class RichTextAreaImplStandard (RichTextAreaImpl):

    def initElement(self):
        print "initElement mozilla"
        iframe = self.elem
        self.onElementInitializing()
        self.isFirstFocus = True
        JS("""
            var iframe = @{{iframe}};
            iframe.onload = function() {
                iframe.onload = null;
                iframe.contentWindow.onfocus = function() {
                    iframe.contentWindow.onfocus = null;
                    iframe.contentWindow.onmouseover = null;
                    iframe.contentWindow.document.designMode = 'On';
                };
                iframe.contentWindow.onmouseover = iframe.contentWindow.onfocus;
                @{{self}}.onElementInitialized();
            };
        """)

