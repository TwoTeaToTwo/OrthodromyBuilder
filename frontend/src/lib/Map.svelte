<script lang="ts">
	import L, { type LeafletMouseEvent } from 'leaflet';

	import pinIcon from "$lib/images/pin.png";

	import { ChosePointState } from './enums';
	import type { Point } from "./types";

	export let point1: Point;
	export let point2: Point;
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
			if (cs == Mercator) {
				point1 = fromWSG84ToMercator([e.latlng.lat, e.latlng.lng]);
			}
			if (cs == WGS84) {
				point1 = [e.latlng.lat, e.latlng.lng];
			}
		}
		
		if (chosingPointState === ChosePointState.ChosingPoint2) {
			if (cs == Mercator) {
				point2 = fromWSG84ToMercator([e.latlng.lat, e.latlng.lng]);
			}
			if (cs == WGS84) {
				point2 = [e.latlng.lat, e.latlng.lng];
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
			map.setMaxBounds([[90, 360], [-90, -360]]);

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

	function updatePoints() {
		if (cs == Mercator) {
			point1 = fromWSG84ToMercator(point1);
			point2 = fromWSG84ToMercator(point2);
		}
		if (cs == WGS84)
		{
			point1 = fromMercatorToWSG84(point1);
			point2 = fromMercatorToWSG84(point2);
		}
	}

	$: if (point1 && point2) {
		pinLayer.clearLayers()
			if (cs == Mercator) {
				L.marker(fromMercatorToWSG84(point1), { icon: pin }).addTo(pinLayer);
				L.marker(fromMercatorToWSG84(point2), { icon: pin }).addTo(pinLayer);
			}
			if (cs == WGS84)
			{
				L.marker(point1, { icon: pin }).addTo(pinLayer);
				L.marker(point2, { icon: pin }).addTo(pinLayer);
			}
	}

	$: if (map && points) {
		polyLineLayer.clearLayers();

		const polylineOptions: L.PolylineOptions = {
			color: '#E4E'
		}
		if (cs == Mercator) {
			console.log(points);
			points = points.map((value) => fromMercatorToWSG84(value));
			console.log(points);
		}
		L.polyline(points, polylineOptions).addTo(polyLineLayer);
	}

	$: if (cs) {
		updatePoints();
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