<template>
    <div>
        <div id="myDiagramDiv" style="width:900px; height:550px; background-color: #DAE4E4;"></div>
    </div>
</template>

<script>
    
    export default {
        mounted(){
            var me = this;
            try{
                me.$nextTick().then(_=>{
                    me.init();
                })
            }
            catch(er){
                console.log(er)
            }
        },
        data(){
            return{}
        },
        methods:{          
            init(){
                var me = this;  
                try{  
                    const myDiagram = new go.Diagram("myDiagramDiv",
                    {
                        "undoManager.isEnabled": true
                    });

                    // the template we defined earlier
                    myDiagram.nodeTemplate =
                    new go.Node("Horizontal",
                        { background: "#44CCFF" })
                        .add(
                        new go.Picture({ margin: 10, width: 50, height: 50, background: "red" })
                            .bind("source"),
                        new go.TextBlock("Default Text",
                            { margin: 12, stroke: "white", font: "bold 16px sans-serif" })
                            .bind("text", "name")
                        );

                    myDiagram.model = new go.TreeModel(
                    [ // the "key" and "parent" property names are required,
                        // but you can add whatever data properties you need for your app
                        { key: "1",              name: "Don Meow",   source: "cat1.png" },
                        { key: "2", parent: "1", name: "Demeter",    source: "cat2.png" },
                        { key: "3", parent: "1", name: "Copricat",   source: "cat3.png" },
                        { key: "4", parent: "3", name: "Jellylorum", source: "cat4.png" },
                        { key: "5", parent: "3", name: "Alonzo",     source: "cat5.png" },
                        { key: "6", parent: "2", name: "Munkustrap", source: "cat6.png" }
                    ]);

                }
                catch(er){
                    console.log(er)
                }
            },      
            refresh(){
                var me = this;  
                try{

                }
                catch(er){
                    console.log(er)
                }
            }
        }

    }
</script>

<style lang="sass" scoped>

</style>