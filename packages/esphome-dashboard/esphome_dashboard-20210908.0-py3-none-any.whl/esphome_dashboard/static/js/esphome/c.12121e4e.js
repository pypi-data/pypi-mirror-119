import{i as o,_ as e,w as t,r as n,n as i,h as s,T as c}from"./c.2c9aeedd.js";import"./c.a3456430.js";import{a}from"./c.33ddc2c5.js";import"./index-9a842255.js";import"./c.c40c8819.js";import"./c.ac6cb6e0.js";import"./c.9f3412f4.js";let r=class extends s{render(){return c`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?c`
              <a
                slot="secondaryAction"
                href="${`./download.bin?configuration=${encodeURIComponent(this.configuration)}`}"
              >
                <mwc-button label="Download"></mwc-button>
              </a>
            `:c`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){if(this._result=o.detail,0!==o.detail)return;const e=document.createElement("a");e.download=this.configuration+".bin",e.href=`./download.bin?configuration=${encodeURIComponent(this.configuration)}`,document.body.appendChild(e),e.click(),e.remove()}_handleRetry(){a(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};r.styles=o`
    a {
      text-decoration: none;
    }
  `,e([t()],r.prototype,"configuration",void 0),e([n()],r.prototype,"_result",void 0),r=e([i("esphome-compile-dialog")],r);
