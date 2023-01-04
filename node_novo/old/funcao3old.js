//FUNCIONA CHAMANDO A FUNÇÃO CONFIGURAINT(), VOU USAR ESTA
function nivelInt(nivel){
 const puppeteer = require('puppeteer');

async function configuraINT(page, num) {
  //acessa a apliccacao INT
  // console.log('#nav > a:nth-child('+num+')');
  
  //await page.waitFor('#nav > a:nth-child(15)');
  //await page.click('#nav > a:nth-child(15)');    
  await page.waitFor('#nav > a:nth-child('+num+')');
  await page.click('#nav > a:nth-child('+num+')');
   
  //Peencher os elementos do coletor
 
  await page.waitFor('#ov-int-app-main > div:nth-child(3) > div.config-panel > div > input:nth-child(1)');
  await page.type('#ov-int-app-main > div:nth-child(3) > div.config-panel > div > input:nth-child(1)','127.0.0.1');

  await page.waitFor('#ov-int-app-main > div:nth-child(3) > div.config-panel > div > input:nth-child(2)');
  await page.type('#ov-int-app-main > div:nth-child(3) > div.config-panel > div > input:nth-child(2)','54321');

  await page.click('#ov-int-app-main > div:nth-child(3) > div.config-button-panel > div');

  // Preencher a whatlist
  
  //host origem
  await page.waitFor('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(2) > label:nth-child(1) > input');
  await page.type('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(2) > label:nth-child(1) > input','10.0.0.1');

  //host destino
  await page.waitFor('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(2) > label:nth-child(2) > input');
  await page.type('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(2) > label:nth-child(2) > input','10.0.0.2');
  
  // port origem e vazio

  //port destino
  await page.waitFor('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(2) > label:nth-child(4) > input');
  await page.type('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(2) > label:nth-child(4) > input','5001');
  
  //seleciona protocolo
  await page.waitFor('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(2) > label:nth-child(5) > select');
  await page.type('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(2) > label:nth-child(5) > select','UDP');


  //Seleciona os níveis de Telemetria
   if(nivel=='minimo'){
     //Somente 3 parametros,  SwitchId,  PortsIDS e Hop Latency
     const tam = 2;
     for(let i=1; i <= tam; i++){
           await page.waitFor('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(3) > label:nth-child('+ i +') > input');
           await page.click('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(3) > label:nth-child('+ i +') > input');
     }
     await page.screenshot({path: 'mim.png'});
     

   } else {
       if (nivel=='medio') {
         //4 parametros, SwitchId,  PortsIDS, Hop Latency e Queue Occupancy
         const tam = 3;
         for(let i=1; i <= tam; i++){
               await page.waitFor('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(3) > label:nth-child('+ i +') > input');
               await page.click('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(3) > label:nth-child('+ i +') > input');
         }
         await page.screenshot({path: 'med.png'});
        
           

         }else{
              // Todos os parametros
                 
	      const tam = 7;
              for(let i=1; i <= tam; i++){
	            await page.waitFor('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(3) > label:nth-child('+ i +') > input');
                    await page.click('#ov-int-app-main > div:nth-child(5) > div:nth-child(2) > div > div:nth-child(3) > label:nth-child('+ i +') > input');
              }
              await page.screenshot({path: 'max.png'});
                 
                   
          }
      }
         
      await page.waitFor('#ov-int-app-main > div:nth-child(5) > div.button-panel > div'),
      await page.click('#ov-int-app-main > div:nth-child(5) > div.button-panel > div')
      //console.log("Fim do configuraINT()");
}


    
(async() => {
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  await page.goto('http://localhost:8181/onos/ui/login.html');

  //logar no site
  await page.type('#username','onos');
  await page.type('#password','rocks');
  await Promise.all([
    page.waitForNavigation(),
    page.click('#submit'),
   
  ]);
    
  //Acessa a barra de pesquisa
  await page.waitFor('#mast > span');
  await page.click('#mast > span');

   //const elemText = await page.$eval('#nav > a:nth-child(14)', elem => elem.innerText);
   const elemText = await page.$eval('#nav > a:nth-child(14)', elem => elem.textContent);

   if(elemText == ' In-band Telemetry Control'){
      //console.log('element innerText 14:', elemText);
      const num = 14
      await configuraINT(page, num);  
   }else{
        //console.log('element innerText 15:', elemText);
        const num = 15
        await configuraINT(page, num);
        }

   await browser.close();

 })()
}//função para passar argumentos

nivelInt(process.argv[2]);
