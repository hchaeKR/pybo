var isMobile = !!navigator.userAgent.match(/(iPhone|iPod|iPad|Android)/i);

function YTClock() {
    this.center = {x: 64, y: 64};
    this.radius = 53.5;
    this.prevSec = -1;
    this.context = null;
}

YTClock.prototype.prepareDom = function() {
    var isIE = /*@cc_on!@*/false;
    if (isIE) {
        return false;
    }
    
    var body = document.getElementsByTagName('body')[0];
    if (body) { 
        var bgCanvas = document.createElement("canvas");
        bgCanvas.setAttribute("width", "128");
        bgCanvas.setAttribute("height", "128");
        bgCanvas.setAttribute("style", "width: 128px; height: 128px;"
                + "position: absolute; left: 0; bottom: 0;"
                + "background-image: url('/static/glass.png')");
        
        var handsCanvas = document.createElement("canvas");
        handsCanvas.setAttribute("width", "128");
        handsCanvas.setAttribute("height", "128");
        handsCanvas.setAttribute("style", "width: 128px; height: 128px;"
                + "position: absolute; left: 0; bottom: 0");
        
        var clockDiv = document.createElement("div");
        clockDiv.setAttribute("id", "ytclock");
        clockDiv.setAttribute("style", "width: 128px; height: 128px;"
                + "position: fixed; left: 27px; bottom: 15px;"
                + "z-index: -1; opacity: 0.9");
        clockDiv.appendChild(bgCanvas);
        clockDiv.appendChild(handsCanvas);
        if (typeof animateOpacity === 'function') {
            animateOpacity(clockDiv, 0.0, 0.9, 0.1, 20);
        }
        body.appendChild(clockDiv);
        
        if (bgCanvas && bgCanvas.getContext) {
            var bgContext = bgCanvas.getContext('2d');
        
            // Draw the ticks.
            bgContext.fillStyle = 'black';
            for (var i = 0; i < 12; i++) {
                bgContext.beginPath();
                var x = this.center.x + this.radius * Math.sin(i / 6.0 * Math.PI);
                var y = this.center.y + this.radius * Math.cos(i / 6.0 * Math.PI);
                bgContext.arc(x, y, 1.5, 0, Math.PI*2, false);
                bgContext.fill();
            }
        }
    
        if (handsCanvas && handsCanvas.getContext) {
            this.context = handsCanvas.getContext('2d');
            
            // Create and initialize shadow.
            this.context.shadowColor = 'black';
            this.context.shadowBlur = 3.0;
            this.context.shadowOffsetX = 0.6;
            this.context.shadowOffsetY = 0.6;
    
            this.update();
            setInterval(function(obj) {obj.update()}, 500, this);
        }
    } else {
        setTimeout(function(obj) {obj.prepareDom()}, 200, this);
    }
}

YTClock.prototype.update = function() {
    var ctx = this.context;
    var centerX = this.center.x;
    var centerY = this.center.y;
    var radius = this.radius;
    
    var now = new Date();
    
    var sec = now.getSeconds();
    if (this.prevSec == sec) {
        return false;
    }
    this.prevSec = sec;
    
    var min = now.getMinutes() + sec / 60.0;
    var hour = now.getHours() + min / 60.0;
    
    var secHeadPos = {
            x:  Math.sin(sec / 30.0 * Math.PI) * radius * 0.90 + centerX,
            y: -Math.cos(sec / 30.0 * Math.PI) * radius * 0.90 + centerY};
    var minHeadPos = {
            x:  Math.sin(min / 30.0 * Math.PI) * radius * 0.85 + centerX,
            y: -Math.cos(min / 30.0 * Math.PI) * radius * 0.85 + centerY};
    var hourHeadPos = {
            x:  Math.sin(hour / 6.0 * Math.PI) * radius * 0.60 + centerX,
            y: -Math.cos(hour / 6.0 * Math.PI) * radius * 0.60 + centerY};
    var secTailPosOut = {
            x: -Math.sin(sec / 30.0 * Math.PI) * radius * 0.20 + centerX,
            y:  Math.cos(sec / 30.0 * Math.PI) * radius * 0.20 + centerY};
    var secTailPosIn = {
            x: -Math.sin(sec / 30.0 * Math.PI) * radius * 0.09 + centerX,
            y:  Math.cos(sec / 30.0 * Math.PI) * radius * 0.09 + centerY};
    var minTailPos = {
            x: -Math.sin(min / 30.0 * Math.PI) * radius * 0.15 + centerX,
            y:  Math.cos(min / 30.0 * Math.PI) * radius * 0.15 + centerY};
    var hourTailPos = {
            x: -Math.sin(hour / 6.0 * Math.PI) * radius * 0.10 + centerX,
            y:  Math.cos(hour / 6.0 * Math.PI) * radius * 0.10 + centerY};
    
    ctx.clearRect(0, 0, 128, 128);

    // Draw the AM/PM string.
    if (!isMobile && ctx.fillText) {
        ctx.fillStyle = 'black';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.font = "12px 'Times New Roman'";
        ctx.fillText(hour < 12 ? 'AM' : 'PM', centerX, centerY + 25.0);
    }
    
    ctx.strokeStyle = 'white';

    // Draw a hour hand.
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.moveTo(hourTailPos.x, hourTailPos.y);
    ctx.lineTo(hourHeadPos.x, hourHeadPos.y);
    ctx.stroke();

    // Draw a min hand.
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(minTailPos.x, minTailPos.y);
    ctx.lineTo(minHeadPos.x, minHeadPos.y);
    ctx.stroke();
    
    ctx.strokeStyle = 'red';
    ctx.fillStyle = 'red';

    // Draw a sec hand.
    ctx.lineWidth = 1.0;
    ctx.beginPath();
    ctx.moveTo(secTailPosOut.x, secTailPosOut.y);
    ctx.lineTo(secHeadPos.x, secHeadPos.y);
    ctx.stroke();

    // Draw the weight on the sec hand.
    ctx.lineWidth = 3.0;
    ctx.beginPath();
    ctx.moveTo(secTailPosOut.x, secTailPosOut.y);
    ctx.lineTo(secTailPosIn.x, secTailPosIn.y);
    ctx.stroke();
    
    // Draw the center dot.
    ctx.beginPath();
    ctx.arc(centerX, centerY, 1.5, 0, Math.PI*2, false);
    ctx.fill();
}

new YTClock().prepareDom();
