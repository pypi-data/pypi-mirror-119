(self["webpackChunkipyparallel_labextension"] = self["webpackChunkipyparallel_labextension"] || []).push([["lab_lib_index_js"],{

/***/ "./lab/lib/clusters.js":
/*!*****************************!*\
  !*** ./lab/lib/clusters.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ClusterManager": () => (/* binding */ ClusterManager)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/domutils */ "webpack/sharing/consume/default/@lumino/domutils");
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_domutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/dragdrop */ "webpack/sharing/consume/default/@lumino/dragdrop");
/* harmony import */ var _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_dragdrop__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/polling */ "webpack/sharing/consume/default/@lumino/polling/@lumino/polling");
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_polling__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _dialog__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./dialog */ "./lab/lib/dialog.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./commands */ "./lab/lib/commands.js");














/**
 * A refresh interval (in ms) for polling the backend cluster manager.
 */
const REFRESH_INTERVAL = 5000;
/**
 * The threshold in pixels to start a drag event.
 */
const DRAG_THRESHOLD = 5;
/**
 * The mimetype used for Jupyter cell data.
 */
const JUPYTER_CELL_MIME = "application/vnd.jupyter.cells";
const CLUSTER_PREFIX = "ipyparallel/clusters";
/**
 * A widget for IPython cluster management.
 */
class ClusterManager extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__.Widget {
    /**
     * Create a new cluster manager.
     */
    constructor(options) {
        super();
        this._dragData = null;
        this._clusters = [];
        this._activeClusterChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_8__.Signal(this);
        this._serverErrorShown = false;
        this._isReady = true;
        this.addClass("ipp-ClusterManager");
        this._serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
        this._injectClientCodeForCluster = options.injectClientCodeForCluster;
        this._getClientCodeForCluster = options.getClientCodeForCluster;
        this._registry = options.registry;
        // A function to set the active cluster.
        this._setActiveById = (id) => {
            const cluster = this._clusters.find((c) => c.id === id);
            if (!cluster) {
                return;
            }
            const old = this._activeCluster;
            if (old && old.id === cluster.id) {
                return;
            }
            this._activeCluster = cluster;
            this._activeClusterChanged.emit({
                name: "cluster",
                oldValue: old,
                newValue: cluster,
            });
            this.update();
        };
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__.PanelLayout());
        this._clusterListing = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__.Widget();
        this._clusterListing.addClass("ipp-ClusterListing");
        // Create the toolbar.
        const toolbar = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Toolbar();
        // Make a label widget for the toolbar.
        const toolbarLabel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__.Widget();
        toolbarLabel.node.textContent = "CLUSTERS";
        toolbarLabel.addClass("ipp-ClusterManager-label");
        toolbar.addItem("label", toolbarLabel);
        // Make a refresh button for the toolbar.
        toolbar.addItem("refresh", new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.refreshIcon,
            onClick: async () => {
                return this._updateClusterList();
            },
            tooltip: "Refresh Cluster List",
        }));
        // Make a new cluster button for the toolbar.
        toolbar.addItem(_commands__WEBPACK_IMPORTED_MODULE_13__.CommandIDs.newCluster, new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.CommandToolbarButton({
            commands: this._registry,
            id: _commands__WEBPACK_IMPORTED_MODULE_13__.CommandIDs.newCluster,
        }));
        layout.addWidget(toolbar);
        layout.addWidget(this._clusterListing);
        // Do an initial refresh of the cluster list.
        void this._updateClusterList();
        // Also refresh periodically.
        this._poll = new _lumino_polling__WEBPACK_IMPORTED_MODULE_7__.Poll({
            factory: async () => {
                await this._updateClusterList();
            },
            frequency: { interval: REFRESH_INTERVAL, backoff: true, max: 60 * 1000 },
            standby: "when-hidden",
        });
    }
    /**
     * The currently selected cluster, or undefined if there is none.
     */
    get activeCluster() {
        return this._activeCluster;
    }
    /**
     * Set an active cluster by id.
     */
    setActiveCluster(id) {
        this._setActiveById(id);
    }
    /**
     * A signal that is emitted when an active cluster changes.
     */
    get activeClusterChanged() {
        return this._activeClusterChanged;
    }
    /**
     * Whether the cluster manager is ready to launch a cluster
     */
    get isReady() {
        return this._isReady;
    }
    /**
     * Get the current clusters known to the manager.
     */
    get clusters() {
        return this._clusters;
    }
    /**
     * Refresh the current list of clusters.
     */
    async refresh() {
        await this._updateClusterList();
    }
    /**
     * Create a new cluster.
     */
    async create() {
        const clusterRequest = await (0,_dialog__WEBPACK_IMPORTED_MODULE_10__.newClusterDialog)({});
        if (!clusterRequest) {
            return;
        }
        const cluster = await this._newCluster(clusterRequest);
        return cluster;
    }
    /**
     * Start a cluster by ID.
     */
    async start(id) {
        const cluster = this._clusters.find((c) => c.id === id);
        if (!cluster) {
            throw Error(`Cannot find cluster ${id}`);
        }
        await this._startById(id);
    }
    /**
     * Stop a cluster by ID.
     */
    async stop(id) {
        const cluster = this._clusters.find((c) => c.id === id);
        if (!cluster) {
            throw Error(`Cannot find cluster ${id}`);
        }
        await this._stopById(id);
    }
    /**
     * Scale a cluster by ID.
     */
    async scale(id) {
        const cluster = this._clusters.find((c) => c.id === id);
        if (!cluster) {
            throw Error(`Cannot find cluster ${id}`);
        }
        const newCluster = await this._scaleById(id);
        return newCluster;
    }
    /**
     * Dispose of the cluster manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._poll.dispose();
        super.dispose();
    }
    /**
     * Handle an update request.
     */
    onUpdateRequest(msg) {
        // Don't bother if the sidebar is not visible
        if (!this.isVisible) {
            return;
        }
        react_dom__WEBPACK_IMPORTED_MODULE_12__.render(react__WEBPACK_IMPORTED_MODULE_11__.createElement(ClusterListing, { clusters: this._clusters, activeClusterId: (this._activeCluster && this._activeCluster.id) || "", scaleById: (id) => {
                return this._scaleById(id);
            }, startById: (id) => {
                return this._startById(id);
            }, stopById: (id) => {
                return this._stopById(id);
            }, setActiveById: this._setActiveById, injectClientCodeForCluster: this._injectClientCodeForCluster }), this._clusterListing.node);
    }
    /**
     * Rerender after showing.
     */
    onAfterShow(msg) {
        this.update();
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        let node = this._clusterListing.node;
        node.addEventListener("p-dragenter", this);
        node.addEventListener("p-dragleave", this);
        node.addEventListener("p-dragover", this);
        node.addEventListener("mousedown", this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        let node = this._clusterListing.node;
        node.removeEventListener("p-dragenter", this);
        node.removeEventListener("p-dragleave", this);
        node.removeEventListener("p-dragover", this);
        node.removeEventListener("mousedown", this);
        document.removeEventListener("mouseup", this, true);
        document.removeEventListener("mousemove", this, true);
    }
    /**
     * Handle the DOM events for the directory listing.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the panel's DOM node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case "mousedown":
                this._evtMouseDown(event);
                break;
            case "mouseup":
                this._evtMouseUp(event);
                break;
            case "mousemove":
                this._evtMouseMove(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `mousedown` events for the widget.
     */
    _evtMouseDown(event) {
        const { button, shiftKey } = event;
        // We only handle main or secondary button actions.
        if (!(button === 0 || button === 2)) {
            return;
        }
        // Shift right-click gives the browser default behavior.
        if (shiftKey && button === 2) {
            return;
        }
        // Find the target cluster.
        const clusterIndex = this._findCluster(event);
        if (clusterIndex === -1) {
            return;
        }
        // Prepare for a drag start
        this._dragData = {
            pressX: event.clientX,
            pressY: event.clientY,
            index: clusterIndex,
        };
        // Enter possible drag mode
        document.addEventListener("mouseup", this, true);
        document.addEventListener("mousemove", this, true);
        event.preventDefault();
    }
    /**
     * Handle the `'mouseup'` event on the document.
     */
    _evtMouseUp(event) {
        // Remove the event listeners we put on the document
        if (event.button !== 0 || !this._drag) {
            document.removeEventListener("mousemove", this, true);
            document.removeEventListener("mouseup", this, true);
        }
        event.preventDefault();
        event.stopPropagation();
    }
    /**
     * Handle the `'mousemove'` event for the widget.
     */
    _evtMouseMove(event) {
        let data = this._dragData;
        if (!data) {
            return;
        }
        // Check for a drag initialization.
        let dx = Math.abs(event.clientX - data.pressX);
        let dy = Math.abs(event.clientY - data.pressY);
        if (dx >= DRAG_THRESHOLD || dy >= DRAG_THRESHOLD) {
            event.preventDefault();
            event.stopPropagation();
            void this._startDrag(data.index, event.clientX, event.clientY);
        }
    }
    /**
     * Start a drag event.
     */
    async _startDrag(index, clientX, clientY) {
        // Create the drag image.
        const model = this._clusters[index];
        const listingItem = this._clusterListing.node.querySelector(`li.ipp-ClusterListingItem[data-cluster-id="${model.id}"]`);
        const dragImage = Private.createDragImage(listingItem);
        // Set up the drag event.
        this._drag = new _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_6__.Drag({
            mimeData: new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.MimeData(),
            dragImage,
            supportedActions: "copy",
            proposedAction: "copy",
            source: this,
        });
        // Add mimeData for plain text so that normal editors can
        // receive the data.
        const textData = this._getClientCodeForCluster(model);
        this._drag.mimeData.setData("text/plain", textData);
        // Add cell data for notebook drops.
        const cellData = [
            {
                cell_type: "code",
                source: textData,
                outputs: [],
                execution_count: null,
                metadata: {},
            },
        ];
        this._drag.mimeData.setData(JUPYTER_CELL_MIME, cellData);
        // Remove mousemove and mouseup listeners and start the drag.
        document.removeEventListener("mousemove", this, true);
        document.removeEventListener("mouseup", this, true);
        return this._drag.start(clientX, clientY).then((action) => {
            if (this.isDisposed) {
                return;
            }
            this._drag = null;
            this._dragData = null;
        });
    }
    /**
     * Launch a new cluster on the server.
     */
    async _newCluster(clusterRequest) {
        this._isReady = false;
        this._registry.notifyCommandChanged(_commands__WEBPACK_IMPORTED_MODULE_13__.CommandIDs.newCluster);
        // TODO: allow requesting a profile, options
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(`${this._serverSettings.baseUrl}${CLUSTER_PREFIX}`, { method: "POST", body: JSON.stringify(clusterRequest) }, this._serverSettings);
        if (response.status !== 200) {
            const err = await response.json();
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Cluster Create Error", err);
            this._isReady = true;
            this._registry.notifyCommandChanged(_commands__WEBPACK_IMPORTED_MODULE_13__.CommandIDs.newCluster);
            throw err;
        }
        const model = (await response.json());
        await this._updateClusterList();
        this._isReady = true;
        this._registry.notifyCommandChanged(_commands__WEBPACK_IMPORTED_MODULE_13__.CommandIDs.newCluster);
        return model;
    }
    /**
     * Refresh the list of clusters on the server.
     */
    async _updateClusterList() {
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(`${this._serverSettings.baseUrl}${CLUSTER_PREFIX}`, {}, this._serverSettings);
        if (response.status !== 200) {
            const msg = "Failed to list clusters: might the server extension not be installed/enabled?";
            const err = new Error(msg);
            if (!this._serverErrorShown) {
                void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("IPP Extension Server Error", err);
                this._serverErrorShown = true;
            }
            throw err;
        }
        const data = (await response.json());
        this._clusters = data;
        // Check to see if the active cluster still exits.
        // If it doesn't, or if there is no active cluster,
        // select the first one.
        const active = this._clusters.find((c) => c.id === (this._activeCluster && this._activeCluster.id));
        if (!active) {
            const id = (this._clusters[0] && this._clusters[0].id) || "";
            this._setActiveById(id);
        }
        this.update();
    }
    /**
     * Start a cluster by its id.
     */
    async _startById(id) {
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(`${this._serverSettings.baseUrl}${CLUSTER_PREFIX}/${id}`, { method: "POST" }, this._serverSettings);
        if (response.status > 299) {
            const err = await response.json();
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Failed to start cluster", err);
            throw err;
        }
        await this._updateClusterList();
    }
    /**
     * Stop a cluster by its id.
     */
    async _stopById(id) {
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(`${this._serverSettings.baseUrl}${CLUSTER_PREFIX}/${id}`, { method: "DELETE" }, this._serverSettings);
        if (response.status !== 204) {
            const err = await response.json();
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Failed to close cluster", err);
            throw err;
        }
        await this._updateClusterList();
    }
    /**
     * Scale a cluster by its id.
     */
    async _scaleById(id) {
        const cluster = this._clusters.find((c) => c.id === id);
        if (!cluster) {
            throw Error(`Failed to find cluster ${id} to scale`);
        }
        // TODO: scale not implemented
        // should add an engine set
        void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Scale not implemented", "");
        // const update = await showScalingDialog(cluster);
        const update = cluster;
        if (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepEqual(update, cluster)) {
            // If the user canceled, or the model is identical don't try to update.
            return Promise.resolve(cluster);
        }
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(`${this._serverSettings.baseUrl}${CLUSTER_PREFIX}/${id}`, {
            method: "PATCH",
            body: JSON.stringify(update),
        }, this._serverSettings);
        if (response.status !== 200) {
            const err = await response.json();
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Failed to scale cluster", err);
            throw err;
        }
        const model = (await response.json());
        await this._updateClusterList();
        return model;
    }
    _findCluster(event) {
        const nodes = Array.from(this.node.querySelectorAll("li.ipp-ClusterListingItem"));
        return _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.ArrayExt.findFirstIndex(nodes, (node) => {
            return _lumino_domutils__WEBPACK_IMPORTED_MODULE_5__.ElementExt.hitTest(node, event.clientX, event.clientY);
        });
    }
}
/**
 * A React component for a launcher button listing.
 */
function ClusterListing(props) {
    let listing = props.clusters.map((cluster) => {
        return (react__WEBPACK_IMPORTED_MODULE_11__.createElement(ClusterListingItem, { isActive: cluster.id === props.activeClusterId, key: cluster.id, cluster: cluster, scale: () => props.scaleById(cluster.id), start: () => props.startById(cluster.id), stop: () => props.stopById(cluster.id), setActive: () => props.setActiveById(cluster.id), injectClientCode: () => props.injectClientCodeForCluster(cluster) }));
    });
    // Return the JSX component.
    return (react__WEBPACK_IMPORTED_MODULE_11__.createElement("div", null,
        react__WEBPACK_IMPORTED_MODULE_11__.createElement("ul", { className: "ipp-ClusterListing-list" }, listing)));
}
/**
 * A TSX functional component for rendering a single running cluster.
 */
function ClusterListingItem(props) {
    const { cluster, isActive, setActive, scale, start, stop, injectClientCode } = props;
    let itemClass = "ipp-ClusterListingItem";
    itemClass = isActive ? `${itemClass} jp-mod-active` : itemClass;
    let cluster_state = "Stopped";
    if (cluster.controller) {
        cluster_state = cluster.controller.state.state;
        if (cluster_state == "after") {
            cluster_state = "Stopped";
        }
    }
    // stop action is 'delete' for already-stopped clusters
    let STOP = cluster_state === "Stopped" ? "DELETE" : "STOP";
    return (react__WEBPACK_IMPORTED_MODULE_11__.createElement("li", { className: itemClass, "data-cluster-id": cluster.id, onClick: (evt) => {
            setActive();
            evt.stopPropagation();
        } },
        react__WEBPACK_IMPORTED_MODULE_11__.createElement("div", { className: "ipp-ClusterListingItem-title" }, cluster.id),
        react__WEBPACK_IMPORTED_MODULE_11__.createElement("div", { className: "ipp-ClusterListingItem-stats" },
            "State: ",
            cluster_state),
        react__WEBPACK_IMPORTED_MODULE_11__.createElement("div", { className: "ipp-ClusterListingItem-stats" },
            "Number of engines: ",
            cluster.engines.n || cluster.cluster.n || "auto"),
        react__WEBPACK_IMPORTED_MODULE_11__.createElement("div", { className: "ipp-ClusterListingItem-button-panel" },
            react__WEBPACK_IMPORTED_MODULE_11__.createElement("button", { className: "ipp-ClusterListingItem-button ipp-ClusterListingItem-code ipp-CodeIcon jp-mod-styled", onClick: (evt) => {
                    injectClientCode();
                    evt.stopPropagation();
                }, title: `Inject client code for ${cluster.id}` }),
            react__WEBPACK_IMPORTED_MODULE_11__.createElement("button", { className: `ipp-ClusterListingItem-button ipp-ClusterListingItem-start jp-mod-styled ${cluster_state == "Stopped" ? "" : "ipp-hidden"}`, onClick: async (evt) => {
                    evt.stopPropagation();
                    return start();
                }, title: `Start ${cluster.id}` }, "START"),
            react__WEBPACK_IMPORTED_MODULE_11__.createElement("button", { className: "ipp-ClusterListingItem-button ipp-ClusterListingItem-scale jp-mod-styled ipp-hidden", onClick: async (evt) => {
                    evt.stopPropagation();
                    return scale();
                }, title: `Rescale ${cluster.id}` }, "SCALE"),
            react__WEBPACK_IMPORTED_MODULE_11__.createElement("button", { className: `ipp-ClusterListingItem-button ipp-ClusterListingItem-stop jp-mod-styled ${cluster_state === "Stopped" && cluster.cluster.cluster_id === ""
                    ? "ipp-hidden"
                    : ""}`, onClick: async (evt) => {
                    evt.stopPropagation();
                    return stop();
                }, title: STOP }, STOP))));
}
/**
 * A namespace for module-private functionality.
 */
var Private;
(function (Private) {
    /**
     * Create a drag image for an HTML node.
     */
    function createDragImage(node) {
        const image = node.cloneNode(true);
        image.classList.add("ipp-ClusterListingItem-drag");
        return image;
    }
    Private.createDragImage = createDragImage;
})(Private || (Private = {}));


/***/ }),

/***/ "./lab/lib/commands.js":
/*!*****************************!*\
  !*** ./lab/lib/commands.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs)
/* harmony export */ });
var CommandIDs;
(function (CommandIDs) {
    /**
     * Inject client code into the active editor.
     */
    CommandIDs.injectClientCode = "ipyparallel:inject-client-code";
    /**
     * Launch a new cluster.
     */
    CommandIDs.newCluster = "ipyparallel:new-cluster";
    /**
     * Launch a new cluster.
     */
    CommandIDs.startCluster = "ipyparallel:start-cluster";
    /**
     * Shutdown a cluster.
     */
    CommandIDs.stopCluster = "ipyparallel:stop-cluster";
    /**
     * Scale a cluster.
     */
    CommandIDs.scaleCluster = "ipyparallel:scale-cluster";
    /**
     * Toggle the auto-starting of clients.
     */
    CommandIDs.toggleAutoStartClient = "ipyparallel:toggle-auto-start-client";
})(CommandIDs || (CommandIDs = {}));


/***/ }),

/***/ "./lab/lib/dialog.js":
/*!***************************!*\
  !*** ./lab/lib/dialog.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NewCluster": () => (/* binding */ NewCluster),
/* harmony export */   "newClusterDialog": () => (/* binding */ newClusterDialog)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);


/**
 * A component for an HTML form that allows the user
 * to select Dialog parameters.
 */
class NewCluster extends react__WEBPACK_IMPORTED_MODULE_1__.Component {
    /**
     * Construct a new NewCluster component.
     */
    constructor(props) {
        super(props);
        let model;
        model = props.initialModel;
        this.state = { model };
    }
    /**
     * When the component updates we take the opportunity to write
     * the state of the cluster to an external object so this can
     * be sent as the result of the dialog.
     */
    componentDidUpdate() {
        let model = Object.assign({}, this.state.model);
        this.props.stateEscapeHatch(model);
    }
    /**
     * React to the number of workers changing.
     */
    onScaleChanged(event) {
        this.setState({
            model: Object.assign(Object.assign({}, this.state.model), { n: parseInt(event.target.value || null, null) }),
        });
    }
    /**
     * React to the number of workers changing.
     */
    onProfileChanged(event) {
        this.setState({
            model: Object.assign(Object.assign({}, this.state.model), { profile: event.target.value }),
        });
    }
    /**
     * React to the number of workers changing.
     */
    onClusterIdChanged(event) {
        this.setState({
            model: Object.assign(Object.assign({}, this.state.model), { cluster_id: event.target.value }),
        });
    }
    /**
     * Render the component..
     */
    render() {
        const model = this.state.model;
        // const disabledClass = "ipp-mod-disabled";
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "ipp-DialogSection" },
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "ipp-DialogSection-item" },
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("span", { className: `ipp-DialogSection-label` }, "Profile"),
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("input", { className: "ipp-DialogInput", value: model.profile, type: "string", placeholder: "default", onChange: (evt) => {
                            this.onProfileChanged(evt);
                        } })),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "ipp-DialogSection-item" },
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("span", { className: `ipp-DialogSection-label` }, "Cluster ID"),
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("input", { className: "ipp-DialogInput", value: model.cluster_id, type: "string", placeholder: "auto", onChange: (evt) => {
                            this.onClusterIdChanged(evt);
                        } })),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "ipp-DialogSection-item" },
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("span", { className: `ipp-DialogSection-label` }, "Engines"),
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("input", { className: "ipp-DialogInput", value: model.n, type: "number", step: "1", placeholder: "auto", onChange: (evt) => {
                            this.onScaleChanged(evt);
                        } })))));
    }
}
/**
 * Show a dialog for Dialog a cluster model.
 *
 * @param model: the initial model.
 *
 * @returns a promse that resolves with the user-selected Dialogs for the
 *   cluster model. If they pressed the cancel button, it resolves with
 *   the original model.
 */
function newClusterDialog(model) {
    let updatedModel = Object.assign({}, model);
    const escapeHatch = (update) => {
        updatedModel = update;
    };
    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
        title: `New Cluster`,
        body: react__WEBPACK_IMPORTED_MODULE_1__.createElement(NewCluster, { initialModel: model, stateEscapeHatch: escapeHatch }),
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: "CREATE" })],
    }).then((result) => {
        if (result.button.accept) {
            return updatedModel;
        }
        else {
            return null;
        }
    });
}


/***/ }),

/***/ "./lab/lib/index.js":
/*!**************************!*\
  !*** ./lab/lib/index.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _sidebar__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./sidebar */ "./lab/lib/sidebar.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../style/index.css */ "./lab/style/index.css");
/* harmony import */ var _style_logo_svg__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../style/logo.svg */ "./lab/style/logo.svg");
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./commands */ "./lab/lib/commands.js");
// IPython Parallel Lab extension derived from dask-labextension@f6141455d770ed7de564fc4aa403b9964cd4e617
// License: BSD-3-Clause













const PLUGIN_ID = "ipyparallel-labextension:plugin";
/**
 * The IPython Parallel extension.
 */
const plugin = {
    activate,
    id: PLUGIN_ID,
    requires: [
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__.IConsoleTracker,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu,
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_6__.INotebookTracker,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry,
        _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__.IStateDB,
    ],
    autoStart: true,
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the cluster launcher plugin.
 */
async function activate(app, commandPalette, consoleTracker, labShell, restorer, mainMenu, notebookTracker, settingRegistry, state) {
    const id = "ipp-cluster-launcher";
    const clientCodeInjector = (model) => {
        const editor = Private.getCurrentEditor(app, notebookTracker, consoleTracker);
        if (!editor) {
            return;
        }
        Private.injectClientCode(model, editor);
    };
    // Create the sidebar panel.
    const sidebar = new _sidebar__WEBPACK_IMPORTED_MODULE_9__.Sidebar({
        clientCodeInjector,
        clientCodeGetter: Private.getClientCode,
        registry: app.commands,
    });
    sidebar.id = id;
    sidebar.title.icon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.LabIcon({
        name: "ipyparallel:logo",
        svgstr: _style_logo_svg__WEBPACK_IMPORTED_MODULE_11__.default,
    });
    // sidebar.title.iconClass = 'ipp-Logo jp-SideBar-tabIcon';
    sidebar.title.caption = "IPython Parallel";
    labShell.add(sidebar, "left", { rank: 200 });
    sidebar.clusterManager.activeClusterChanged.connect(async () => {
        const active = sidebar.clusterManager.activeCluster;
        return state.save(id, {
            cluster: active ? active.id : "",
        });
    });
    // A function to create a new client for a session.
    const createClientForSession = async (session) => {
        if (!session) {
            return;
        }
        const cluster = sidebar.clusterManager.activeCluster;
        if (!cluster || !(await Private.shouldUseKernel(session.kernel))) {
            return;
        }
        return Private.createClientForKernel(cluster, session.kernel);
    };
    // An array of the trackers to check for active sessions.
    const trackers = [
        notebookTracker,
        consoleTracker,
    ];
    // A function to recreate a client on reconnect.
    const injectOnSessionStatusChanged = async (sessionContext) => {
        if (sessionContext.session &&
            sessionContext.session.kernel &&
            sessionContext.session.kernel.status === "restarting") {
            return createClientForSession(sessionContext.session);
        }
    };
    // A function to inject a client when a new session owner is added.
    const injectOnWidgetAdded = (_, widget) => {
        widget.sessionContext.statusChanged.connect(injectOnSessionStatusChanged);
    };
    // A function to inject a client when the active cluster changes.
    const injectOnClusterChanged = () => {
        trackers.forEach((tracker) => {
            tracker.forEach(async (widget) => {
                const session = widget.sessionContext.session;
                if (session && (await Private.shouldUseKernel(session.kernel))) {
                    return createClientForSession(session);
                }
            });
        });
    };
    // Whether the cluster clients should aggressively inject themselves
    // into the current session.
    let autoStartClient = false;
    // Update the existing trackers and signals in light of a change to the
    // settings system. In particular, this reacts to a change in the setting
    // for auto-starting cluster client.
    const updateTrackers = () => {
        // Clear any existing signals related to the auto-starting.
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_8__.Signal.clearData(injectOnWidgetAdded);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_8__.Signal.clearData(injectOnSessionStatusChanged);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_8__.Signal.clearData(injectOnClusterChanged);
        if (autoStartClient) {
            // When a new console or notebook is created, inject
            // a new client into it.
            trackers.forEach((tracker) => {
                tracker.widgetAdded.connect(injectOnWidgetAdded);
            });
            // When the status of an existing notebook changes, reinject the client.
            trackers.forEach((tracker) => {
                tracker.forEach(async (widget) => {
                    await createClientForSession(widget.sessionContext.session);
                    widget.sessionContext.statusChanged.connect(injectOnSessionStatusChanged);
                });
            });
            // When the active cluster changes, reinject the client.
            sidebar.clusterManager.activeClusterChanged.connect(injectOnClusterChanged);
        }
    };
    // Fetch the initial state of the settings.
    void Promise.all([settingRegistry.load(PLUGIN_ID), state.fetch(id)]).then(async (res) => {
        const settings = res[0];
        if (!settings) {
            console.warn("Unable to retrieve ipp-labextension settings");
            return;
        }
        const state = res[1];
        const cluster = state ? state.cluster : "";
        const onSettingsChanged = () => {
            // Determine whether to use the auto-starting client.
            autoStartClient = settings.get("autoStartClient").composite;
            updateTrackers();
        };
        onSettingsChanged();
        // React to a change in the settings.
        settings.changed.connect(onSettingsChanged);
        // If an active cluster is in the state, reset it.
        if (cluster) {
            await sidebar.clusterManager.refresh();
            sidebar.clusterManager.setActiveCluster(cluster);
        }
    });
    // Add a command to inject client connection code for a given cluster model.
    // This looks for a cluster model in the application context menu,
    // and looks for an editor among the currently active notebooks and consoles.
    // If either is not found, it bails.
    app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.injectClientCode, {
        label: "Inject IPython Client Connection Code",
        execute: () => {
            const cluster = Private.clusterFromClick(app, sidebar.clusterManager);
            if (!cluster) {
                return;
            }
            clientCodeInjector(cluster);
        },
    });
    // Add a command to launch a new cluster.
    app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.newCluster, {
        label: (args) => (args["isPalette"] ? "Create New Cluster" : "NEW"),
        execute: () => sidebar.clusterManager.create(),
        iconClass: (args) => args["isPalette"] ? "" : "jp-AddIcon jp-Icon jp-Icon-16",
        isEnabled: () => sidebar.clusterManager.isReady,
        caption: () => {
            if (sidebar.clusterManager.isReady) {
                return "Start New Cluster";
            }
            return "Cluster starting...";
        },
    });
    // Add a command to launch a new cluster.
    app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.startCluster, {
        label: "Start Cluster",
        execute: () => {
            const cluster = Private.clusterFromClick(app, sidebar.clusterManager);
            if (!cluster) {
                return;
            }
            return sidebar.clusterManager.start(cluster.id);
        },
    });
    // Add a command to stop a cluster.
    app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.stopCluster, {
        label: "Shutdown Cluster",
        execute: () => {
            const cluster = Private.clusterFromClick(app, sidebar.clusterManager);
            if (!cluster) {
                return;
            }
            return sidebar.clusterManager.stop(cluster.id);
        },
    });
    // Add a command to resize a cluster.
    app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.scaleCluster, {
        label: "Scale Cluster…",
        execute: () => {
            const cluster = Private.clusterFromClick(app, sidebar.clusterManager);
            if (!cluster) {
                return;
            }
            return sidebar.clusterManager.scale(cluster.id);
        },
    });
    // Add a command to toggle the auto-starting client code.
    app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.toggleAutoStartClient, {
        label: "Auto-Start IPython Parallel",
        isToggled: () => autoStartClient,
        execute: async () => {
            const value = !autoStartClient;
            const key = "autoStartClient";
            return settingRegistry
                .set(PLUGIN_ID, key, value)
                .catch((reason) => {
                console.error(`Failed to set ${PLUGIN_ID}:${key} - ${reason.message}`);
            });
        },
    });
    // Add some commands to the menu and command palette.
    mainMenu.settingsMenu.addGroup([
        { command: _commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.toggleAutoStartClient },
    ]);
    [_commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.newCluster, _commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.toggleAutoStartClient].forEach((command) => {
        commandPalette.addItem({
            category: "IPython Parallel",
            command,
            args: { isPalette: true },
        });
    });
    // Add a context menu items.
    app.contextMenu.addItem({
        command: _commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.injectClientCode,
        selector: ".ipp-ClusterListingItem",
        rank: 10,
    });
    app.contextMenu.addItem({
        command: _commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.stopCluster,
        selector: ".ipp-ClusterListingItem",
        rank: 3,
    });
    app.contextMenu.addItem({
        command: _commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.scaleCluster,
        selector: ".ipp-ClusterListingItem",
        rank: 2,
    });
    app.contextMenu.addItem({
        command: _commands__WEBPACK_IMPORTED_MODULE_12__.CommandIDs.startCluster,
        selector: ".ipp-ClusterListing-list",
        rank: 1,
    });
}
var Private;
(function (Private) {
    /**
     * A private counter for ids.
     */
    Private.id = 0;
    /**
     * Whether a kernel should be used. Only evaluates to true
     * if it is valid and in python.
     */
    async function shouldUseKernel(kernel) {
        if (!kernel) {
            return false;
        }
        const spec = await kernel.spec;
        return !!spec && spec.language.toLowerCase().indexOf("python") !== -1;
    }
    Private.shouldUseKernel = shouldUseKernel;
    /**
     * Connect a kernel to a cluster by creating a new Client.
     */
    async function createClientForKernel(model, kernel) {
        const code = getClientCode(model);
        const content = {
            store_history: false,
            code,
        };
        return new Promise((resolve, _) => {
            const future = kernel.requestExecute(content);
            future.onIOPub = (msg) => {
                if (msg.header.msg_type !== "display_data") {
                    return;
                }
                resolve(void 0);
            };
        });
    }
    Private.createClientForKernel = createClientForKernel;
    /**
     * Insert code to connect to a given cluster.
     */
    function injectClientCode(cluster, editor) {
        const cursor = editor.getCursorPosition();
        const offset = editor.getOffsetAt(cursor);
        const code = getClientCode(cluster);
        editor.model.value.insert(offset, code);
    }
    Private.injectClientCode = injectClientCode;
    /**
     * Get code to connect to a given cluster.
     */
    function getClientCode(cluster) {
        return `import ipyparallel as ipp

cluster = ipp.Cluster.from_file("${cluster.cluster_file}")
rc = cluster.connect_client_sync()
rc`;
    }
    Private.getClientCode = getClientCode;
    /**
     * Get the currently focused kernel in the application,
     * checking both notebooks and consoles.
     */
    function getCurrentKernel(shell, notebookTracker, consoleTracker) {
        var _a, _b, _c, _d;
        // Get a handle on the most relevant kernel,
        // whether it is attached to a notebook or a console.
        let current = shell.currentWidget;
        let kernel;
        if (current && notebookTracker.has(current)) {
            kernel = (_a = current.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        }
        else if (current && consoleTracker.has(current)) {
            kernel = (_b = current.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel;
        }
        else if (notebookTracker.currentWidget) {
            const current = notebookTracker.currentWidget;
            kernel = (_c = current.sessionContext.session) === null || _c === void 0 ? void 0 : _c.kernel;
        }
        else if (consoleTracker.currentWidget) {
            const current = consoleTracker.currentWidget;
            kernel = (_d = current.sessionContext.session) === null || _d === void 0 ? void 0 : _d.kernel;
        }
        return kernel;
    }
    Private.getCurrentKernel = getCurrentKernel;
    /**
     * Get the currently focused editor in the application,
     * checking both notebooks and consoles.
     * In the case of a notebook, it creates a new cell above the currently
     * active cell and then returns that.
     */
    function getCurrentEditor(app, notebookTracker, consoleTracker) {
        // Get a handle on the most relevant kernel,
        // whether it is attached to a notebook or a console.
        let current = app.shell.currentWidget;
        let editor;
        if (current && notebookTracker.has(current)) {
            _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_6__.NotebookActions.insertAbove(current.content);
            const cell = current.content.activeCell;
            editor = cell && cell.editor;
        }
        else if (current && consoleTracker.has(current)) {
            const cell = current.console.promptCell;
            editor = cell && cell.editor;
        }
        else if (notebookTracker.currentWidget) {
            const current = notebookTracker.currentWidget;
            _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_6__.NotebookActions.insertAbove(current.content);
            const cell = current.content.activeCell;
            editor = cell && cell.editor;
        }
        else if (consoleTracker.currentWidget) {
            const current = consoleTracker.currentWidget;
            const cell = current.console.promptCell;
            editor = cell && cell.editor;
        }
        return editor;
    }
    Private.getCurrentEditor = getCurrentEditor;
    /**
     * Get a cluster model based on the application context menu click node.
     */
    function clusterFromClick(app, manager) {
        const test = (node) => !!node.dataset.clusterId;
        const node = app.contextMenuHitTest(test);
        if (!node) {
            return undefined;
        }
        const id = node.dataset.clusterId;
        return manager.clusters.find((cluster) => cluster.id === id);
    }
    Private.clusterFromClick = clusterFromClick;
})(Private || (Private = {}));


/***/ }),

/***/ "./lab/lib/sidebar.js":
/*!****************************!*\
  !*** ./lab/lib/sidebar.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Sidebar": () => (/* binding */ Sidebar)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _clusters__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./clusters */ "./lab/lib/clusters.js");


/**
 * A widget for hosting IPP cluster widgets
 */
class Sidebar extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Create a new IPP sidebar.
     */
    constructor(options) {
        super();
        this.addClass("ipp-Sidebar");
        let layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.PanelLayout());
        const injectClientCodeForCluster = options.clientCodeInjector;
        const getClientCodeForCluster = options.clientCodeGetter;
        // Add the cluster manager component.
        this._clusters = new _clusters__WEBPACK_IMPORTED_MODULE_1__.ClusterManager({
            registry: options.registry,
            injectClientCodeForCluster,
            getClientCodeForCluster,
        });
        layout.addWidget(this._clusters);
    }
    /**
     * Get the cluster manager associated with the sidebar.
     */
    get clusterManager() {
        return this._clusters;
    }
}


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./lab/style/index.css":
/*!*******************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./lab/style/index.css ***!
  \*******************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/getUrl.js */ "./node_modules/css-loader/dist/runtime/getUrl.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _code_light_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./code-light.svg */ "./lab/style/code-light.svg");
/* harmony import */ var _code_light_svg__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_code_light_svg__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _code_dark_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./code-dark.svg */ "./lab/style/code-dark.svg");
/* harmony import */ var _code_dark_svg__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_code_dark_svg__WEBPACK_IMPORTED_MODULE_4__);
// Imports





var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
var ___CSS_LOADER_URL_REPLACEMENT_0___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()((_code_light_svg__WEBPACK_IMPORTED_MODULE_3___default()));
var ___CSS_LOADER_URL_REPLACEMENT_1___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()((_code_dark_svg__WEBPACK_IMPORTED_MODULE_4___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ":root {\n  --ipp-launch-button-height: 24px;\n}\n\n/**\n * Rules related to the overall sidebar panel.\n */\n\n.ipp-Sidebar {\n  background: var(--jp-layout-color1);\n  color: var(--jp-ui-font-color1);\n  font-size: var(--jp-ui-font-size1);\n  overflow: auto;\n}\n\n/**\n * Rules related to the cluster manager.\n */\n\n.ipp-ClusterManager {\n  border-top: 6px solid var(--jp-toolbar-border-color);\n}\n\n.ipp-ClusterManager .jp-Toolbar {\n  align-items: center;\n}\n\n.ipp-ClusterManager .jp-Toolbar .ipp-ClusterManager-label {\n  flex: 0 0 auto;\n  font-weight: 600;\n  text-transform: uppercase;\n  letter-spacing: 1px;\n  font-size: var(--jp-ui-font-size0);\n  padding: 8px 8px 8px 12px;\n  margin: 0px;\n}\n\n.ipp-ClusterManager button.jp-Button > span {\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n}\n\n.ipp-ClusterListing ul.ipp-ClusterListing-list {\n  list-style-type: none;\n  padding: 0;\n  margin: 0;\n}\n\n.ipp-ClusterListingItem {\n  display: inline-block;\n  list-style-type: none;\n  padding: 8px;\n  width: 100%;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  cursor: grab;\n}\n\n.ipp-ClusterListingItem-drag {\n  opacity: 0.7;\n  color: var(--jp-ui-font-color1);\n  cursor: grabbing;\n  max-width: 260px;\n  transform: translateX(-50%) translateY(-50%);\n}\n\n.ipp-ClusterListingItem-title {\n  margin: 0px;\n  font-size: var(--jp-ui-font-size2);\n}\n\n.ipp-ClusterListingItem-link a {\n  text-decoration: none;\n  color: var(--jp-content-link-color);\n}\n\n.ipp-ClusterListingItem-link a:hover {\n  text-decoration: underline;\n}\n\n.ipp-ClusterListingItem-link a:visited {\n  color: var(--jp-content-link-color);\n}\n\n.ipp-ClusterListingItem:hover {\n  background: var(--jp-layout-color2);\n}\n\n.ipp-ClusterListingItem.jp-mod-active {\n  color: white;\n  background: var(--jp-brand-color0);\n}\n\n.ipp-ClusterListingItem.jp-mod-active a,\n.ipp-ClusterListingItem.jp-mod-active a:visited {\n  color: white;\n}\n\n.ipp-ClusterListingItem button.jp-mod-styled {\n  background-color: transparent;\n}\n\n.ipp-ClusterListingItem button.jp-mod-styled:hover {\n  background-color: var(--jp-layout-color3);\n}\n\n.ipp-ClusterListingItem.jp-mod-active button.jp-mod-styled:hover {\n  background-color: var(--jp-brand-color1);\n}\n\n.ipp-ClusterListingItem-button-panel {\n  display: flex;\n  align-content: center;\n}\n\nbutton.ipp-ClusterListingItem-stop {\n  color: var(--jp-warn-color1);\n  font-weight: 600;\n}\n\nbutton.ipp-ClusterListingItem-scale {\n  color: var(--jp-accent-color1);\n  font-weight: 600;\n}\n\nbutton.ipp-ClusterListingItem-start {\n  color: var(--jp-accent-color1);\n  font-weight: 600;\n}\n\nbutton.ipp-hidden {\n  display: none;\n}\n\n.ipp-ClusterListingItem button.ipp-ClusterListingItem-code.jp-mod-styled {\n  margin: 0 4px 0 4px;\n  background-repeat: no-repeat;\n  background-position: center;\n}\n\n/**\n * Rules for the scaling dialog.\n */\n\n.ipp-DialogHeader {\n  font-size: var(--jp-ui-font-size2);\n}\n\n.ipp-DialogSection {\n  margin-left: 24px;\n}\n\n.ipp-DialogSection-item {\n  display: flex;\n  align-items: center;\n  justify-content: space-around;\n  margin: 12px 0 12px 0;\n}\n\n.ipp-DialogHeader input[type=\"checkbox\"] {\n  position: relative;\n  top: 4px;\n  left: 4px;\n  margin: 0 0 0 8px;\n}\n\n.ipp-DialogSection input[type=\"number\"] {\n  width: 72px;\n}\n\n.ipp-DialogSection-label.ipp-mod-disabled {\n  color: var(--jp-ui-font-color3);\n}\n\n.ipp-DialogSection input[type=\"number\"]:disabled {\n  color: var(--jp-ui-font-color3);\n}\n\n/**\n * Rules for the logos.\n */\n\n.ipp-SearchIcon {\n  background-image: var(--jp-icon-search);\n}\n\n[data-jp-theme-light=\"true\"] .ipp-CodeIcon {\n  background-image: url(" + ___CSS_LOADER_URL_REPLACEMENT_0___ + ");\n}\n\n[data-jp-theme-light=\"false\"] .ipp-CodeIcon {\n  background-image: url(" + ___CSS_LOADER_URL_REPLACEMENT_1___ + ");\n}\n\n.ipp-ClusterListingItem.jp-mod-active .ipp-CodeIcon {\n  background-image: url(" + ___CSS_LOADER_URL_REPLACEMENT_1___ + ");\n}\n", "",{"version":3,"sources":["webpack://./lab/style/index.css"],"names":[],"mappings":"AAAA;EACE,gCAAgC;AAClC;;AAEA;;EAEE;;AAEF;EACE,mCAAmC;EACnC,+BAA+B;EAC/B,kCAAkC;EAClC,cAAc;AAChB;;AAEA;;EAEE;;AAEF;EACE,oDAAoD;AACtD;;AAEA;EACE,mBAAmB;AACrB;;AAEA;EACE,cAAc;EACd,gBAAgB;EAChB,yBAAyB;EACzB,mBAAmB;EACnB,kCAAkC;EAClC,yBAAyB;EACzB,WAAW;AACb;;AAEA;EACE,aAAa;EACb,mBAAmB;EACnB,mBAAmB;AACrB;;AAEA;EACE,qBAAqB;EACrB,UAAU;EACV,SAAS;AACX;;AAEA;EACE,qBAAqB;EACrB,qBAAqB;EACrB,YAAY;EACZ,WAAW;EACX,mBAAmB;EACnB,gBAAgB;EAChB,uBAAuB;EACvB,YAAY;AACd;;AAEA;EACE,YAAY;EACZ,+BAA+B;EAC/B,gBAAgB;EAChB,gBAAgB;EAChB,4CAA4C;AAC9C;;AAEA;EACE,WAAW;EACX,kCAAkC;AACpC;;AAEA;EACE,qBAAqB;EACrB,mCAAmC;AACrC;;AAEA;EACE,0BAA0B;AAC5B;;AAEA;EACE,mCAAmC;AACrC;;AAEA;EACE,mCAAmC;AACrC;;AAEA;EACE,YAAY;EACZ,kCAAkC;AACpC;;AAEA;;EAEE,YAAY;AACd;;AAEA;EACE,6BAA6B;AAC/B;;AAEA;EACE,yCAAyC;AAC3C;;AAEA;EACE,wCAAwC;AAC1C;;AAEA;EACE,aAAa;EACb,qBAAqB;AACvB;;AAEA;EACE,4BAA4B;EAC5B,gBAAgB;AAClB;;AAEA;EACE,8BAA8B;EAC9B,gBAAgB;AAClB;;AAEA;EACE,8BAA8B;EAC9B,gBAAgB;AAClB;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,mBAAmB;EACnB,4BAA4B;EAC5B,2BAA2B;AAC7B;;AAEA;;EAEE;;AAEF;EACE,kCAAkC;AACpC;;AAEA;EACE,iBAAiB;AACnB;;AAEA;EACE,aAAa;EACb,mBAAmB;EACnB,6BAA6B;EAC7B,qBAAqB;AACvB;;AAEA;EACE,kBAAkB;EAClB,QAAQ;EACR,SAAS;EACT,iBAAiB;AACnB;;AAEA;EACE,WAAW;AACb;;AAEA;EACE,+BAA+B;AACjC;;AAEA;EACE,+BAA+B;AACjC;;AAEA;;EAEE;;AAEF;EACE,uCAAuC;AACzC;;AAEA;EACE,yDAAqC;AACvC;;AAEA;EACE,yDAAoC;AACtC;;AAEA;EACE,yDAAoC;AACtC","sourcesContent":[":root {\n  --ipp-launch-button-height: 24px;\n}\n\n/**\n * Rules related to the overall sidebar panel.\n */\n\n.ipp-Sidebar {\n  background: var(--jp-layout-color1);\n  color: var(--jp-ui-font-color1);\n  font-size: var(--jp-ui-font-size1);\n  overflow: auto;\n}\n\n/**\n * Rules related to the cluster manager.\n */\n\n.ipp-ClusterManager {\n  border-top: 6px solid var(--jp-toolbar-border-color);\n}\n\n.ipp-ClusterManager .jp-Toolbar {\n  align-items: center;\n}\n\n.ipp-ClusterManager .jp-Toolbar .ipp-ClusterManager-label {\n  flex: 0 0 auto;\n  font-weight: 600;\n  text-transform: uppercase;\n  letter-spacing: 1px;\n  font-size: var(--jp-ui-font-size0);\n  padding: 8px 8px 8px 12px;\n  margin: 0px;\n}\n\n.ipp-ClusterManager button.jp-Button > span {\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n}\n\n.ipp-ClusterListing ul.ipp-ClusterListing-list {\n  list-style-type: none;\n  padding: 0;\n  margin: 0;\n}\n\n.ipp-ClusterListingItem {\n  display: inline-block;\n  list-style-type: none;\n  padding: 8px;\n  width: 100%;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  cursor: grab;\n}\n\n.ipp-ClusterListingItem-drag {\n  opacity: 0.7;\n  color: var(--jp-ui-font-color1);\n  cursor: grabbing;\n  max-width: 260px;\n  transform: translateX(-50%) translateY(-50%);\n}\n\n.ipp-ClusterListingItem-title {\n  margin: 0px;\n  font-size: var(--jp-ui-font-size2);\n}\n\n.ipp-ClusterListingItem-link a {\n  text-decoration: none;\n  color: var(--jp-content-link-color);\n}\n\n.ipp-ClusterListingItem-link a:hover {\n  text-decoration: underline;\n}\n\n.ipp-ClusterListingItem-link a:visited {\n  color: var(--jp-content-link-color);\n}\n\n.ipp-ClusterListingItem:hover {\n  background: var(--jp-layout-color2);\n}\n\n.ipp-ClusterListingItem.jp-mod-active {\n  color: white;\n  background: var(--jp-brand-color0);\n}\n\n.ipp-ClusterListingItem.jp-mod-active a,\n.ipp-ClusterListingItem.jp-mod-active a:visited {\n  color: white;\n}\n\n.ipp-ClusterListingItem button.jp-mod-styled {\n  background-color: transparent;\n}\n\n.ipp-ClusterListingItem button.jp-mod-styled:hover {\n  background-color: var(--jp-layout-color3);\n}\n\n.ipp-ClusterListingItem.jp-mod-active button.jp-mod-styled:hover {\n  background-color: var(--jp-brand-color1);\n}\n\n.ipp-ClusterListingItem-button-panel {\n  display: flex;\n  align-content: center;\n}\n\nbutton.ipp-ClusterListingItem-stop {\n  color: var(--jp-warn-color1);\n  font-weight: 600;\n}\n\nbutton.ipp-ClusterListingItem-scale {\n  color: var(--jp-accent-color1);\n  font-weight: 600;\n}\n\nbutton.ipp-ClusterListingItem-start {\n  color: var(--jp-accent-color1);\n  font-weight: 600;\n}\n\nbutton.ipp-hidden {\n  display: none;\n}\n\n.ipp-ClusterListingItem button.ipp-ClusterListingItem-code.jp-mod-styled {\n  margin: 0 4px 0 4px;\n  background-repeat: no-repeat;\n  background-position: center;\n}\n\n/**\n * Rules for the scaling dialog.\n */\n\n.ipp-DialogHeader {\n  font-size: var(--jp-ui-font-size2);\n}\n\n.ipp-DialogSection {\n  margin-left: 24px;\n}\n\n.ipp-DialogSection-item {\n  display: flex;\n  align-items: center;\n  justify-content: space-around;\n  margin: 12px 0 12px 0;\n}\n\n.ipp-DialogHeader input[type=\"checkbox\"] {\n  position: relative;\n  top: 4px;\n  left: 4px;\n  margin: 0 0 0 8px;\n}\n\n.ipp-DialogSection input[type=\"number\"] {\n  width: 72px;\n}\n\n.ipp-DialogSection-label.ipp-mod-disabled {\n  color: var(--jp-ui-font-color3);\n}\n\n.ipp-DialogSection input[type=\"number\"]:disabled {\n  color: var(--jp-ui-font-color3);\n}\n\n/**\n * Rules for the logos.\n */\n\n.ipp-SearchIcon {\n  background-image: var(--jp-icon-search);\n}\n\n[data-jp-theme-light=\"true\"] .ipp-CodeIcon {\n  background-image: url(code-light.svg);\n}\n\n[data-jp-theme-light=\"false\"] .ipp-CodeIcon {\n  background-image: url(code-dark.svg);\n}\n\n.ipp-ClusterListingItem.jp-mod-active .ipp-CodeIcon {\n  background-image: url(code-dark.svg);\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./lab/style/logo.svg":
/*!****************************!*\
  !*** ./lab/style/logo.svg ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg\n   xmlns=\"http://www.w3.org/2000/svg\"\n   version=\"1.1\"\n   viewBox=\"0 0 20 20\"\n   height=\"20\"\n   width=\"20\">\n   <!-- text: IP in Source Code Pro -->\n    <g\n       aria-label=\"IP\">\n      <path\n         class=\"jp-icon3 jp-icon-selectable\"\n         fill=\"#616161\"\n         d=\"m 1.619125,15.248 v -1.136 h 2.608 V 5.8720001 h -2.608 v -1.12 h 6.56 v 1.12 h -2.608 V 14.112 h 2.608 v 1.136 z\" />\n      <path\n         class=\"jp-icon3 jp-icon-selectable\"\n         fill=\"#616161\"\n         d=\"M 11.324875,15.248 V 4.7520001 h 3.168 q 1.168,0 2.032,0.288 0.88,0.288 1.36,0.976 0.496,0.672 0.496,1.824 0,1.104 -0.496,1.824 -0.48,0.7199999 -1.36,1.0719999 -0.88,0.352 -2.032,0.352 h -1.84 v 4.16 z m 1.328,-5.248 h 1.68 q 1.376,0 2.032,-0.5119999 0.672,-0.528 0.672,-1.648 0,-1.136 -0.672,-1.568 -0.672,-0.448 -2.032,-0.448 h -1.68 z\" />\n  </g>\n</svg>\n");

/***/ }),

/***/ "./lab/style/index.css":
/*!*****************************!*\
  !*** ./lab/style/index.css ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./lab/style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__.default, options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__.default.locals || {});

/***/ }),

/***/ "./lab/style/code-dark.svg":
/*!*********************************!*\
  !*** ./lab/style/code-dark.svg ***!
  \*********************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23E0E0E0' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath fill='none' d='M0 0h24v24H0V0z'/%3E%3Cpath d='M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z'/%3E%3C/svg%3E"

/***/ }),

/***/ "./lab/style/code-light.svg":
/*!**********************************!*\
  !*** ./lab/style/code-light.svg ***!
  \**********************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23616161' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath fill='none' d='M0 0h24v24H0V0z'/%3E%3Cpath d='M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z'/%3E%3C/svg%3E"

/***/ })

}]);
//# sourceMappingURL=lab_lib_index_js.13974db8d324932308c0.js.map