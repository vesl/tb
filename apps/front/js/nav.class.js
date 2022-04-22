// NavApp class
class NavApp {
    
    constructor(app){
        this.app = app
        this.li = this.createLi()
        this.button = this.createButton()
        this.div = this.createDiv()
    }
    
    createLi(){
        return $('<li>').addClass('mb-1')
    }
    
    createButton(){
        return $('<button>')
                .addClass('btn btn-toggle align-items-center rounded collapsed')
                .attr('data-bs-toggle','collapse')
                .attr('data-bs-target','#'+this.app.toLowerCase())
                .attr('aria-expanded','false')
                .text(this.app)
    }
    
    createDiv(){
        return $('<div>')
            .addClass('collapse')
            .attr('id',this.app.toLowerCase())
    }
    
    render(){
        return this.li
            .append(this.button)
            .append(this.div)
    }
}

// SubNav class
class SubNav {
    
    constructor(appSubNav,click) {
        this.appSubNav = appSubNav
        this.click = click
        this.ul = this.createUl()
        this.li = this.createLi()
        this.a = this.createA()
    }
    
    createUl(){
        return $('<ul>')
            .addClass('btn-toggle-nav list-unstyled fw-normal pb-1 small')
    }

    createLi(){
        return $('<li>')
    }
                       
    createA(){
        return $('<a>')
            .attr('href','#')
            .addClass('link-dark rounded')
            .click(this.click)
            .text(this.appSubNav)
    }
    
    render(){
        return this.ul.append(this.li.append(this.a))
    }
}