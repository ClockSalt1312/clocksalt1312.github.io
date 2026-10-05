/* ============================================================
 * 盐津虾 VIP · 卡密激活模块（vip.js）
 * 纯前端方案：代码里只存卡密的加盐 SHA-256 哈希，不存明文。
 * 卡密哈希 -> 有效天数。新增卡密：把哈希加到下表即可。
 * ============================================================ */
const VIP_CODES = {
  '0e2c245a43bf70cceb02a0905451eecb4f2f73e4a4c4c5b38fbefae6d5c04c73': 30,  // 月卡①
  'f12a598b44951230df025fe846f58c7d36722274ae6588221f011187f0b9c476': 30,  // 月卡②
  '24a46a2f558f4fce140dbb58c0f8a3fdc0e6f6b9c3c7f766233e52e3c5465582': 90,  // 季卡①
  'e427046b03c50b053dd4966ae6b7c5af6cd366961ab6c811067273d2df78454e': 90,  // 季卡②
  '283a4eb195ca2d1d03a1a1c30cdeae2e356a44b683f723453b2c8152a182438e': 365, // 年卡①
  '0532da06d0e5bbfd45cc247b390f66b7e77059e16caa958bf6e2633bcc6a3c69': 30,  // 月卡③
  'dd15f1d68422da1fd6b0bf8c576f1d3e57a2d53616b4b471cec0ec4f6a09ed1b': 30,  // 月卡④
  '355296b87b2dcc02050fc6de17d32c56b9476d8b38a3072f59abe3c873088541': 30,  // 月卡⑤
  '222fa8bcb3e8af43090a0db695a3b375a58ab288e2ef5ec7cfcd03e343911082': 30,  // 月卡⑥
  'e2c285bf7a76fca58e26decfbae919207b72a396d363b7dc76f52e973d249a2b': 30,  // 月卡⑦
  'c259f823e04c019db0073e7527f53b89caeec4aec33f2bb8cee43a06eb469468': 30,  // 月卡⑧
  'b108f1c3442a5d3cded3d00d8b326301bc2c8a0fb4ce8e9a689d0210253ad5f2': 30,  // 月卡⑨
  'c60860a6162cb76b75c4c84c4c86fff85276da016b2d276d472ab4f98bc36f4b': 30,  // 月卡⑩
  '375fa68d574edd7e1e53b22ec70d1ea2cf3eba19e1080eebe10039f89c81f0d5': 90,  // 季卡③
  'bb02bba05515a7fbe00dc0d093c6ec6ea482d9d8e174fae21422e848133e690a': 90,  // 季卡④
  '41f9167c26d56336321010cf0ebab35d454d1aa548051955700d0579b9b45ebc': 90,  // 季卡⑤
  '064e8de2a5a249b4ea24b78285ad4605d4c2bc7a29dd2fedb16ed6146bd11dd0': 90,  // 季卡⑥
  '4b7ef5380e7bcb035d3755fd16819ab032cee32da434bc1aac17f3768d45ceb8': 90,  // 季卡⑦
  'e22d6897b343af7ef47128f4bc5761b7d46cd39d40c544f1d27e092f694d09ce': 90,  // 季卡⑧
  '5313dad007712f9c3c17cdbdeaeb321f389719d78032348dff523647b8024e94': 90,  // 季卡⑨
  '4838f786fedc760d03d09bb74892801874cff8709165c28fd6e1e08af603af12': 90,  // 季卡⑩
  '593f33e354269adbd169fb07eae6a26162868c1cb2a7da37457c44d7270e2c08': 365,  // 年卡②
  '468a1d8673f7b1657ec68282d7fa5b59bd7fc66e9c5853540390371cf07e052e': 365,  // 年卡③
  'c39f334d6496427bb9a157ada9e30f340cfa9241b8b2f67d4de025822cf31451': 365,  // 年卡④
  '38e5883cf153f362a37905755ccab907af911621cd2b68537e391eb593309138': 365,  // 年卡⑤
  'fcabc8c22b98b329220518cb8cc19cafff97ee12ce6bf5d2286d2f1e59efe502': 365,  // 年卡⑥
};

const VIP_KEY = 'sos_vip_v1';
const VIP_SALT = 'YJX::';

/* 卡密激活开放时间：2027/03/01（此前为预购阶段，激活入口关闭） */
const VIP_OPEN_AT = new Date('2027-03-01T00:00:00+08:00').getTime();
function vipActivationOpen(){
  return Date.now() >= VIP_OPEN_AT;
}

function vipNormalize(code){
  return String(code || '').trim().toUpperCase().replace(/\s+/g, '');
}

async function vipSha256(text){
  if(!window.crypto || !crypto.subtle) throw new Error('no-crypto');
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

/* 查询当前 VIP 状态：{ expire } 或 null；过期记录自动清除 */
function getVip(){
  try{
    const v = JSON.parse(localStorage.getItem(VIP_KEY) || 'null');
    if(v && typeof v.expire === 'number'){
      if(v.expire > Date.now()) return v;
      localStorage.removeItem(VIP_KEY); /* 到期自动取消 */
    }
  }catch(e){}
  return null;
}

function vipExpireText(){
  const v = getVip();
  if(!v) return '';
  const d = new Date(v.expire);
  return d.getFullYear() + '/' + String(d.getMonth() + 1).padStart(2, '0') + '/' + String(d.getDate()).padStart(2, '0');
}

/* 已使用过的卡密哈希名单（防止同一张卡密反复激活累加时长） */
const VIP_USED_KEY = 'sos_vip_used_v1';
function vipUsedList(){
  try{
    const a = JSON.parse(localStorage.getItem(VIP_USED_KEY) || '[]');
    return Array.isArray(a) ? a : [];
  }catch(e){ return []; }
}
function vipMarkUsed(hash){
  try{
    const a = vipUsedList();
    if(a.indexOf(hash) === -1){
      a.push(hash);
      localStorage.setItem(VIP_USED_KEY, JSON.stringify(a));
    }
  }catch(e){}
}

/* 激活卡密。返回 { ok, days, expire, reason } */
async function redeemVipCode(code){
  const norm = vipNormalize(code);
  if(!norm) return { ok:false, reason:'empty' };
  let hash;
  try{
    hash = await vipSha256(VIP_SALT + norm);
  }catch(e){
    return { ok:false, reason:'crypto' };
  }
  const days = VIP_CODES[hash];
  if(!days) return { ok:false, reason:'invalid' };
  /* 同一张卡密只能激活一次 */
  if(vipUsedList().indexOf(hash) !== -1) return { ok:false, reason:'used' };
  const now = Date.now();
  /* 用另一张卡密续费则叠加时长 */
  let expire = now + days * 864e5;
  const cur = getVip();
  if(cur) expire = cur.expire + days * 864e5;
  try{ localStorage.setItem(VIP_KEY, JSON.stringify({ h: hash, expire: expire })); }catch(e){}
  vipMarkUsed(hash);
  return { ok:true, days:days, expire:expire };
}
