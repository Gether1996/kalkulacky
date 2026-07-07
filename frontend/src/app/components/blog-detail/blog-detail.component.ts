import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { BlogService } from '../../services/blog.service';
import { BlogPostDetail } from '../../models/blog.models';
import { SeoService } from '../../services/seo.service';

@Component({
  selector: 'app-blog-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './blog-detail.component.html',
  styleUrls: ['./blog-detail.component.css']
})
export class BlogDetailComponent implements OnInit {
  post: BlogPostDetail | null = null;
  safeHtmlContent: SafeHtml | null = null;
  loading: boolean = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private blogService: BlogService,
    private sanitizer: DomSanitizer,
    private seo: SeoService
  ) {}

  ngOnInit() {
    // Load on the server too — the blog is SEO content and must render into the
    // SSR HTML so crawlers/social scrapers see the article (blog.service points
    // at the internal backend URL during SSR).
    const slug = this.route.snapshot.paramMap.get('slug');
    if (slug) {
      this.loadPost(slug);
    }
  }

  loadPost(slug: string) {
    this.loading = true;
    this.error = null;

    this.blogService.getPost(slug).subscribe({
      next: (data) => {
        this.post = data;
        this.safeHtmlContent = this.sanitizer.bypassSecurityTrustHtml(data.content_html);
        this.applySeo(data);
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading post:', err);
        this.error = 'Blog príspevok sa nenašiel';
        this.loading = false;
      }
    });
  }

  private applySeo(post: BlogPostDetail) {
    this.seo.apply({
      title: post.title,
      description: post.excerpt || post.title,
      path: `/blog/${post.slug}`,
      keywords: post.meta_keywords || undefined,
    });
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('sk-SK', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  getCalculatorRoute(calculatorSlug: string): string {
    return `/calculator/${calculatorSlug}`;
  }
}
