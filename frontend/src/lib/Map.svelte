<script lang="ts">
	import L, { type LeafletMouseEvent } from 'leaflet';

	import pinIcon from "$lib/images/pin.png";

	import { ChosePointState } from './enums';
	import type { Point } from "./types";

	export let point1: Point;
	export let point2: Point;
	export let gpoint1: Point;
	export let gpoint2: Point;
	export let points: Point[];
	export let chosingPointState: ChosePointState;
	export let cs: string;

	let map: L.Map | null;

	const PinIcon = L.Icon.extend({
		options: {
			iconSize: [40, 40],
			iconAnchor: [20, 40],
			iconUrl: pinIcon
		}
	});

	const pin = new PinIcon();
	const pinLayer = L.layerGroup();
	const polyLineLayer = L.layerGroup();

	let tileProviders = new Map<string, L.TileLayer>();

	const WGS84 = "EPSG:4326";
	const sk72 = "EPSG:4284";
	const Mercator = "EPSG:3857";

	function onMapClick(e: LeafletMouseEvent) {
		if (chosingPointState === ChosePointState.ChosingPoint1) {
			point1 = [e.latlng.lat, e.latlng.lng];
			if (cs == Mercator) {
				gpoint1 = fromWSG84ToMercator(point1);
			}
			if (cs == WGS84) {
				gpoint1 = point1;
			}
		}
		
		if (chosingPointState === ChosePointState.ChosingPoint2) {
			point2 = [e.latlng.lat, e.latlng.lng];
			if (cs == Mercator) {
				gpoint2 = fromWSG84ToMercator(point2);
			}
			if (cs == WGS84) {
				gpoint2 = point2;
			}
		}

		chosingPointState = ChosePointState.Standby;
	}

	function initTileProviders() {
		const defaultTileProvider = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
		});
		tileProviders.set("default", defaultTileProvider);

		const lightTileProvider = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
			subdomains: 'abcd',
		});
		tileProviders.set("light", lightTileProvider);

		const darkTileProvider = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
			subdomains: 'abcd',
		});
		tileProviders.set("dark", darkTileProvider);

		const sateliteTileProvider = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
			attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
		});
		tileProviders.set("satelite", sateliteTileProvider);
	}

	function initMap(map: L.Map | null) {
		if (!map)
			throw Error("Can't init null, expect L.Map!");
		else
		{
			let tile = tileProviders.get("default");

			if (tile)
				tile.addTo(map);
			else
				throw Error("Tile provider not found");

			pinLayer.addTo(map);
			polyLineLayer.addTo(map);

			map.attributionControl.setPrefix(false);

			map.setView([0, 0], 1);
			map.setMaxBounds([[90, 180], [-90, -180]]);

			map.on("click", onMapClick);
		}
	}

	function createMap(container: HTMLDivElement) {
		const options: L.MapOptions = {
			preferCanvas: true,
			minZoom: 3,
		};
		const map = L.map(container, options);
		
		initTileProviders();
		initMap(map);

		return map;
	}

	function useMap(container: HTMLDivElement) {
		map = createMap(container);

		return {
			destroy: () => {
				if (map) {
					map.remove();
					map = null;
				}
			}
		}
	}
	
	function fromMercatorToWSG84(point: Point) {
		let res_point: Point;
		let x = point[0];
		let y = point[1];
		x = (x * 180) / 20037508.34;
		y = (y * 180) / 20037508.34;
		y = (Math.atan(Math.pow(Math.E, y * (Math.PI / 180))) * 360) / Math.PI - 90;
		res_point = [x, y];
		return res_point;
	}

	function fromWSG84ToMercator(point: Point){
		let res_point: Point;
		let x = point[0];
		let y = point[1];
		x = (x * 20037508.34) / 180.0;
		y = Math.log(Math.tan(((90 + y) * Math.PI) / 360)) / (Math.PI / 180);
		y = (y * 20037508.34) / 180;
		res_point = [x, y];
		return res_point;
	}

	function addLineWithBounds(points: Point[], polylineOptions: L.PolylineOptions, polyLineLayer: L.LayerGroup)
	{
		const lat_bound = 85;
		const lng_bound = 180;
		let prev = points[0];
		for (let i = 1; i < points.length; i++) {
			let current_point = points[i];
			let prev_sign = prev[1] < 0;
			let sign = current_point[1] < 0;
			if ((Math.abs(current_point[0]) < lat_bound)
			 && (Math.abs(current_point[1]) < lng_bound)
			 && (((Math.abs(current_point[1]) + Math.abs(prev[1])) < (lng_bound * 1.8))
			 || (prev_sign == sign))) {
				let line = [prev, current_point];
				L.polyline(line, polylineOptions).addTo(polyLineLayer);
			}
			prev = current_point;
		}
	}

	$: if (point1 && point2) {
		pinLayer.clearLayers();
		L.marker(point1, { icon: pin }).addTo(pinLayer);
		L.marker(point2, { icon: pin }).addTo(pinLayer);
	}

	$: if (map && points) {
		polyLineLayer.clearLayers();

		const polylineOptions: L.PolylineOptions = {
			color: '#E4E'
		}

		addLineWithBounds(points, polylineOptions, polyLineLayer);
	}
	
</script>


<link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
   integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
   crossorigin=""/>
<div class="map" use:useMap></div>

<style>
	.map {
		position: fixed;
		top: 0;
		left: 0;
		
		width: 100vw;
		height: 100vh;
	}
</style>