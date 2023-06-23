function loginC()
{
    let frm = document.querySelector('form')//폼 데이터를 받음
    id = frm[0]                 //각 값 할당
    pw = frm[1]
    if(!id.value)
    {
        document.getElementById("checkid").className = "valid-note"
        id.focus()
        return false
    }
    else
    {
        document.getElementById("checkid").className = "invalid-note"
    }
    if(!pw.value)
    {
        document.getElementById("checkpw").className = "valid-note"
        pw.focus()
        return false
    }
    else
    {
        document.getElementById("checkpw").className = "invalid-note"
    }
    return true
}

var checked = 0

function idCheck()
{
    id = document.getElementById('id')
    str = document.getElementById('ids').value
    chk = "'" + document.getElementById('id').value + "'"
    str = str.replace(/\{'user_id':/g, '')
    console.log(str)
    console.log(id)
    console.log(!str.includes(id))
    if(!!id.value && !str.includes(chk))
    {
        checked = 1
        document.getElementById('cid').className = 'invalid-note'
        document.getElementById('nid').className = 'invalid-note'
        document.getElementById('yid').className = 'yid'
    }
    else
    {
        checked = 0
        document.getElementById('cid').className = 'invalid-note'
        document.getElementById('yid').className = 'invalid-note'
        document.getElementById('nid').className = 'nid'
    }
}

function regiC()
{
    input = document.querySelectorAll('input') //input 데이터를 받음
    id = input[0]               //각 값 할당
    pw = input[1]
    pwc = input[2]
    email = input[3]
    if(checked !== 1)
    {
        document.getElementById('nid').className = 'invalid-note'
        document.getElementById('yid').className = 'invalid-note'
        document.getElementById('cid').className = 'nid'
        document.getElementById('id').focus()
        return false
    }
    if(!pw.value || pw.value !== pwc.value)
    {
        document.getElementById("checkema").className = "invalid-note"
        document.getElementById("checkpwc").className = "valid-note"
        document.getElementById('pw').focus()
        document.getElementById('pwc').focus()
        return false
    }
    else
    {
    }
    if(!email.value)
    {
        document.getElementById("checkpwc").className = "invalid-note"
        document.getElementById("checkema").className = "valid-note"
        document.getElementById('email').focus()
        return false
    }
    return true
}

function regiC2()
{
    input = document.querySelectorAll('input') //input 데이터를 받음
    console.log(input)

    if(input[0].checked)
    {
        gender = input[0]
    }
    else if(input[1].checked)
    {
        gender = input[1]
    }
    else
    {
        document.getElementById("cgender").className = "valid-note"
        gender.focus()
        return false
    }
    pname = input[2]
    age = parseInt(input[3].value)
    height = parseInt(input[4].value)
    weight = parseInt(input[5].value)

    console.log(age)
    console.log(height)
    console.log(weight)

        // document.getElementById("gender").className = "invalid-note"
    if(!pname.value)
    {
        document.getElementById("cage").className = "invalid-note"
        document.getElementById("cheight").className = "invalid-note"
        document.getElementById("cweight").className = "invalid-note"
        document.getElementById("cgender").className = "invalid-note"
        document.getElementById("cname").className = "valid-note"
        document.getElementById("name").focus()
        return false
    }

    if(!age || typeof(age) != 'number' || age > 100)
    {

        document.getElementById("cheight").className = "invalid-note"
        document.getElementById("cname").className = "invalid-note"
        document.getElementById("cweight").className = "invalid-note"
        document.getElementById("cgender").className = "invalid-note"
        document.getElementById("cage").className = "valid-note"
        document.getElementById("age").focus()
        return false
    }
    if(!height || typeof(height) != 'number' || height > 250)
    {
        document.getElementById("cage").className = "invalid-note"
        document.getElementById("cname").className = "invalid-note"
        document.getElementById("cweight").className = "invalid-note"
        document.getElementById("cgender").className = "invalid-note"
        document.getElementById("cheight").className = "valid-note"
        document.getElementById("cheight").focus()
        return false
    }
    if(!weight || typeof(weight) != 'number' || weight > 200)
    {
        document.getElementById("cage").className = "invalid-note"
        document.getElementById("cname").className = "invalid-note"
        document.getElementById("cheight").className = "invalid-note"
        document.getElementById("cgender").className = "invalid-note"
        document.getElementById("cweight").className = "valid-note"
        document.getElementById("cweight").focus()
        return false
    }
    return true
}

function changepw()
{
    input = document.querySelectorAll('input')
    ppw = input[0]
    npw = input[1]
    npwc = input[2]
    if(!ppw.value || !npw.value || !npwc.value)
    {
        document.getElementById("cpw").className = "invalid-note"
        document.getElementById("mt").className = "valid-note"
        return false
    }
    if(npw.value !== npwc.value)
    {
        document.getElementById("mt").className = "invalid-note"
        document.getElementById("cpw").className = "valid-note"
        document.getElementById('npwc').focus()
        return false
    }
    return true
}

function idfind()
{
     input = document.querySelectorAll('input')
    femail = input[0]
    if(!femail.value)
    {
        document.getElementById("mt").className = "valid-note"
        return false
    }
    return true
}

function findpw()
{
     input = document.querySelectorAll('input')
    id = input[0]
    if(!id.value)
    {
        document.getElementById("mt").className = "valid-note"
        return false
    }
    return true
}

function findpwex()
{
    input = document.querySelectorAll('input')
    npw = input[0]
    npwc = input[1]
    if(!npw.value || !npwc.value)
    {
        document.getElementById("cpw").className = "invalid-note"
        document.getElementById("mt").className = "valid-note"
        return false
    }
    if(npw.value !== npwc.value)
    {
        document.getElementById("mt").className = "invalid-note"
        document.getElementById("cpw").className = "valid-note"
        document.getElementById('npwc').focus()
        return false
    }
    return true
}

function hasCheck()
{
    first = document.getElementById('stalle')
    second = document.getElementById('ndalle')
    third = document.getElementById('rdalle')
    if(document.querySelector('input[id = allergy]').checked)
    {
        if(!first.value && !second.value && !third.value)
        {
            document.getElementById("calle").className = "valid-note"
            return false
        }
    }
    return true
}

function ingreanal()
{
    document.getElementById('sub').value = 'ingre'
    console.log('ingre')
    document.getElementById('main').submit()
}

function nutrianal()
{
    document.getElementById('sub').value = 'nutri'
    console.log('nutri')
    document.getElementById('main').submit()
}

function exercise(value)
{
    document.getElementById('exerindex').textContent = value
    if(value < 30)
    {
        document.getElementById('exertext').textContent = "가벼운 활동(사무실에서 일보기)"
    }
    else if(value < 35)
    {
        document.getElementById('exertext').textContent = "보통 활동(청소등의 가사일)"
    }
    else if(value < 41)
    {
        document.getElementById('exertext').textContent = "육체활동(농사 및 운동, 신체활동이 많음)"
    }
}