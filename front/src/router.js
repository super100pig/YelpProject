import Vue from 'vue'
import Router from 'vue-router'
import Frame from "@/components/Frame";
import Graph from "@/components/Graph";
import AttributeGraph from "@/components/AttributeGraph";
import DeviceTable from "@/components/DeviceTable";
import NodeTable from "@/components/NodeTable"
import EdgeTable from "@/components/EdgeTable"
import Notification from "@/components/Notification";
import UploadPage from "@/components/UploadPage";
import StationGraph from "@/components/StationGraph";

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            children: [
                {
                    path: 'uploadPage',
                    component: UploadPage
                }, {
                    path: 'attributeGraph',
                    component: AttributeGraph
                }, {
                    path: 'graph',
                    component: Graph
                }, {
                    path: 'stationGraph',
                    component: StationGraph
                }, {
                    path: 'deviceTable',
                    component: DeviceTable
                }, {
                    path: 'stationGraph',
                    component: StationGraph
                }, {
                    path: 'notification',
                    component: Notification
                }, {
                    path: 'nodeTable',
                    component: NodeTable
                }, {
                    path: 'edgeTable',
                    component: EdgeTable
                }
            ],
            component: Frame,
            redirect: 'uploadPage'
        }
    ]
})
